# -*- coding: utf-8 -*-
from flask import request, jsonify
import traceback
from api.service.tarefa_service import TarefaService
from api.utils.error_response import ErrorResponse

"""
Classe responsável por controlar os endpoints da API REST para a entidade Tarefa.

Implementa métodos de CRUD, utilizando injeção de dependência
para receber a instância de TarefaService, desacoplando a lógica de negócio
da camada de controle.
"""
class TarefaControl:
    def __init__(self, tarefa_service: TarefaService):
        """
        Construtor da classe TarefaControl
        :param tarefa_service: Instância do TarefaService (injeção de dependência)
        """
        print("⬆️  TarefaControl.constructor()")
        self.__tarefa_service = tarefa_service

    def store(self, usuario_id: int = None):
        """Cria uma nova tarefa para o usuário autenticado"""
        print("🔵 TarefaControl.store()")
        try:
            json_tarefa = request.json.get("tarefa")
            if not json_tarefa:
                return jsonify({
                    "success": False,
                    "error": {
                        "message": "Dados da tarefa não fornecidos",
                        "code": 400
                    }
                }), 400

            # ✅ CORREÇÃO: Agora passa o usuario_id como usuario_atribuidor_id
            # O usuario_responsavel_id deve vir do JSON da requisição
            newIdTarefa = self.__tarefa_service.createTarefa(json_tarefa, usuario_id)
            
            return jsonify({
                "success": True,
                "message": "Tarefa criada com sucesso",
                "data": {
                    "tarefa": {
                        "id": newIdTarefa,
                        "titulo": json_tarefa.get("titulo"),
                        "descricao": json_tarefa.get("descricao"),
                        "status": json_tarefa.get("status", "pendente"),
                        "prioridade": json_tarefa.get("prioridade", "media"),
                        "concluida": json_tarefa.get("concluida", False),
                        "data_limite": json_tarefa.get("data_limite"),
                        "data_inicio": json_tarefa.get("data_inicio"),
                        "data_fim": json_tarefa.get("data_fim"),
                        "projeto_id": json_tarefa.get("projeto_id"),
                        # ✅ CORREÇÃO: Novos campos
                        "usuario_responsavel_id": json_tarefa.get("usuario_responsavel_id"),
                        "usuario_atribuidor_id": usuario_id,  # Quem criou a tarefa
                        "data_criacao": json_tarefa.get("data_criacao"),
                        "data_atualizacao": json_tarefa.get("data_atualizacao")
                    }
                }
            }), 201
        except ErrorResponse as e:
            return jsonify({
                "success": False,
                "error": {
                    "message": e.message,
                    "details": e.details,
                    "code": e.status_code
                }
            }), e.status_code
        except Exception as e:
            print(f"❌ Erro inesperado em store: {traceback.format_exc()}")
            return jsonify({
                "success": False,
                "error": {
                    "message": "Erro interno no servidor",
                    "code": 500
                }
            }), 500

    def index(self, usuario_id: int = None):
        """Lista todas as tarefas onde o usuário é RESPONSÁVEL"""
        print("🔵 TarefaControl.index()")
        try:
            # ✅ CORREÇÃO: Passa o usuario_id para buscar apenas tarefas onde usuário é RESPONSÁVEL
            lista_tarefas = self.__tarefa_service.findAll(usuario_id)
            return jsonify({
                "success": True,
                "message": "Executado com sucesso",
                "data": {"tarefas": lista_tarefas}
            }), 200
        except ErrorResponse as e:
            return jsonify({
                "success": False,
                "error": {
                    "message": e.message,
                    "details": e.details,
                    "code": e.status_code
                }
            }), e.status_code
        except Exception as e:
            print(f"❌ Erro inesperado em index: {traceback.format_exc()}")
            return jsonify({
                "success": False,
                "error": {
                    "message": "Erro interno no servidor",
                    "code": 500
                }
            }), 500

    def show(self, id, usuario_id: int = None):
        """Busca uma tarefa pelo ID (só retorna se usuário for RESPONSÁVEL)"""
        print("🔵 TarefaControl.show()")
        try:
            # ✅ CORREÇÃO: Passa o usuario_id para verificar se usuário é RESPONSÁVEL
            tarefa = self.__tarefa_service.findById(id, usuario_id)
            return jsonify({
                "success": True,
                "message": "Executado com sucesso",
                "data": tarefa
            }), 200
        except ErrorResponse as e:
            return jsonify({
                "success": False,
                "error": {
                    "message": e.message,
                    "details": e.details,
                    "code": e.status_code
                }
            }), e.status_code
        except Exception as e:
            print(f"❌ Erro inesperado em show: {traceback.format_exc()}")
            return jsonify({
                "success": False,
                "error": {
                    "message": "Erro interno no servidor",
                    "code": 500
                }
            }), 500

    def update(self, id, usuario_id: int = None):
        """Atualiza os dados de uma tarefa existente (só se usuário for RESPONSÁVEL)"""
        print("🔵 TarefaControl.update()")
        try:
            # ✅ CORREÇÃO: Agora verifica se o usuário é o RESPONSÁVEL pela tarefa
            tarefa_atualizada = self.__tarefa_service.updateTarefa(id, request.json, usuario_id)

            # ✅ CORREÇÃO: Busca a tarefa atualizada para retornar dados completos
            tarefa_atualizada_data = self.__tarefa_service.findById(id, usuario_id)

            return jsonify({
                "success": True,
                "message": "Tarefa atualizada com sucesso",
                "data": {
                    "tarefa": tarefa_atualizada_data
                }
            }), 200
        except ErrorResponse as e:
            return jsonify({
                "success": False,
                "error": {
                    "message": e.message,
                    "details": e.details,
                    "code": e.status_code
                }
            }), e.status_code
        except Exception as e:
            print(f"❌ Erro inesperado em update: {traceback.format_exc()}")
            return jsonify({
                "success": False,
                "error": {
                    "message": "Erro interno no servidor",
                    "code": 500
                }
            }), 500

    def destroy(self, id, usuario_id: int = None):
        """Remove uma tarefa pelo ID (só se usuário for RESPONSÁVEL)"""
        print("🔵 TarefaControl.destroy()")
        try:
            # ✅ CORREÇÃO: Passa o usuario_id para verificar se usuário é RESPONSÁVEL
            excluiu = self.__tarefa_service.deleteTarefa(id, usuario_id)
            return jsonify({
                "success": True,
                "message": "Tarefa excluída com sucesso"
            }), 200
        except ErrorResponse as e:
            return jsonify({
                "success": False,
                "error": {
                    "message": e.message,
                    "details": e.details,
                    "code": e.status_code
                }
            }), e.status_code
        except Exception as e:
            print(f"❌ Erro inesperado em destroy: {traceback.format_exc()}")
            return jsonify({
                "success": False,
                "error": {
                    "message": "Erro interno no servidor",
                    "code": 500
                }
            }), 500

    def show_by_projeto(self, projeto_id, usuario_id: int = None):
        """Lista todas as tarefas de um projeto específico (só se usuário for RESPONSÁVEL)"""
        print("🔵 TarefaControl.show_by_projeto()")
        try:
            # ✅ CORREÇÃO: Passa o usuario_id para verificar se usuário é RESPONSÁVEL
            tarefas = self.__tarefa_service.findByProjetoId(projeto_id, usuario_id)
            return jsonify({
                "success": True,
                "message": "Executado com sucesso",
                "data": {"tarefas": tarefas}
            }), 200
        except ErrorResponse as e:
            return jsonify({
                "success": False,
                "error": {
                    "message": e.message,
                    "details": e.details,
                    "code": e.status_code
                }
            }), e.status_code
        except Exception as e:
            print(f"❌ Erro inesperado em show_by_projeto: {traceback.format_exc()}")
            return jsonify({
                "success": False,
                "error": {
                    "message": "Erro interno no servidor",
                    "code": 500
                }
            }), 500

    def marcar_concluida(self, id, usuario_id: int = None):
        """Marca uma tarefa como concluída (só se usuário for RESPONSÁVEL)"""
        print("🔵 TarefaControl.marcar_concluida()")
        try:
            # ✅ CORREÇÃO CRÍTICA: Corrigido o método chamado
            # O método correto é updateTarefaConcluida, não marcarConcluida
            request_body = {
                "tarefa": {
                    "concluida": True,
                    "status": "concluida"
                }
            }
            tarefa_concluida = self.__tarefa_service.updateTarefaConcluida(id, request_body, usuario_id)
            
            # ✅ CORREÇÃO: Busca a tarefa atualizada para retornar dados completos
            tarefa_atualizada = self.__tarefa_service.findById(id, usuario_id)
            
            return jsonify({
                "success": True,
                "message": "Tarefa marcada como concluída com sucesso!",
                "data": {
                    "tarefa": tarefa_atualizada
                }
            }), 200
            
        except ErrorResponse as e:
            return jsonify({
                "success": False,
                "error": {
                    "message": e.message,
                    "details": e.details,
                    "code": e.status_code
                }
            }), e.status_code
        except Exception as e:
            print(f"❌ Erro inesperado em marcar_concluida: {traceback.format_exc()}")
            return jsonify({
                "success": False,
                "error": {
                    "message": "Erro interno no servidor",
                    "code": 500
                }
            }), 500

    def count_tarefas(self, usuario_id: int = None):
        """Retorna estatísticas das tarefas onde usuário é RESPONSÁVEL"""
        print("🔵 TarefaControl.count_tarefas()")
        try:
            # ✅ CORREÇÃO: Busca tarefas onde o usuário é RESPONSÁVEL
            tarefas = self.__tarefa_service.findAll(usuario_id)
            
            total = len(tarefas)
            concluidas = len([t for t in tarefas if t.get('concluida')])
            pendentes = total - concluidas
            
            # Contar por prioridade
            prioridades = {
                "alta": 0,
                "media": 0,
                "baixa": 0
            }
            
            for tarefa in tarefas:
                prioridade = tarefa.get('prioridade', 'media')
                if prioridade in prioridades:
                    prioridades[prioridade] += 1

            # Contar por status
            status_count = {}
            for tarefa in tarefas:
                status = tarefa.get('status', 'pendente')
                status_count[status] = status_count.get(status, 0) + 1

            return jsonify({
                "success": True,
                "message": "Estatísticas calculadas com sucesso",
                "data": {
                    "total": total,
                    "concluidas": concluidas,
                    "pendentes": pendentes,
                    "por_prioridade": prioridades,
                    "por_status": status_count,
                    "taxa_conclusao": round((concluidas / total * 100), 2) if total > 0 else 0,
                    "contexto": "Tarefas onde você é responsável"
                }
            }), 200
        except ErrorResponse as e:
            return jsonify({
                "success": False,
                "error": {
                    "message": e.message,
                    "details": e.details,
                    "code": e.status_code
                }
            }), e.status_code
        except Exception as e:
            print(f"❌ Erro inesperado em count_tarefas: {traceback.format_exc()}")
            return jsonify({
                "success": False,
                "error": {
                    "message": "Erro interno no servidor",
                    "code": 500
                }
            }), 500
        
    def minhas_tarefas_responsavel(self, usuario_id: int = None):
        """Lista todas as tarefas onde o usuário é o RESPONSÁVEL"""
        print("🔵 TarefaControl.minhas_tarefas_responsavel()")
        try:
            # ✅ CORREÇÃO: Usa o método que busca por usuario_responsavel_id
            lista_tarefas = self.__tarefa_service.findAll(usuario_id)
            return jsonify({
                "success": True,
                "message": "Tarefas onde você é responsável",
                "data": {"tarefas": lista_tarefas}
            }), 200
        except ErrorResponse as e:
            return jsonify({
                "success": False,
                "error": {
                    "message": e.message,
                    "details": e.details,
                    "code": e.status_code
                }
            }), e.status_code
        except Exception as e:
            print(f"❌ Erro inesperado em minhas_tarefas_responsavel: {traceback.format_exc()}")
            return jsonify({
                "success": False,
                "error": {
                    "message": "Erro interno no servidor",
                    "code": 500
                }
            }), 500

    def tarefas_atribuidas(self, usuario_id: int = None):
        """Lista todas as tarefas que o usuário ATRIBUIU para outros"""
        print("🔵 TarefaControl.tarefas_atribuidas()")
        try:
            # ✅ CORREÇÃO: Busca tarefas onde usuario_atribuidor_id = usuario_id
            # Mas usuario_responsavel_id != usuario_id (tarefas atribuídas para outros)
            lista_tarefas = self.__tarefa_service.findByField("usuario_atribuidor_id", usuario_id)
            
            # Filtra apenas as tarefas atribuídas para outros (não auto-atribuição)
            tarefas_atribuidas = [t for t in lista_tarefas if t.get('usuario_responsavel_id') != usuario_id]
            
            return jsonify({
                "success": True,
                "message": "Tarefas que você atribuiu para outros",
                "data": {"tarefas": tarefas_atribuidas}
            }), 200
        except ErrorResponse as e:
            return jsonify({
                "success": False,
                "error": {
                    "message": e.message,
                    "details": e.details,
                    "code": e.status_code
                }
            }), e.status_code
        except Exception as e:
            print(f"❌ Erro inesperado em tarefas_atribuidas: {traceback.format_exc()}")
            return jsonify({
                "success": False,
                "error": {
                    "message": "Erro interno no servidor",
                    "code": 500
                }
            }), 500

    def toggle_concluida(self, id, usuario_id: int = None):
        """Alterna o status de conclusão da tarefa (só se usuário for RESPONSÁVEL)"""
        print("🔵 TarefaControl.toggle_concluida()")
        try:
            # Busca a tarefa atual para verificar o status
            tarefa_atual = self.__tarefa_service.findById(id, usuario_id)
            if not tarefa_atual:
                return jsonify({
                    "success": False,
                    "error": {
                        "message": "Tarefa não encontrada",
                        "code": 404
                    }
                }), 404

            # Alterna o status de concluída
            nova_concluida = not tarefa_atual.get('concluida', False)
            novo_status = "concluida" if nova_concluida else "pendente"
            
            request_body = {
                "tarefa": {
                    "concluida": nova_concluida,
                    "status": novo_status
                }
            }
            
            tarefa_atualizada = self.__tarefa_service.updateTarefaConcluida(id, request_body, usuario_id)
            
            # Busca a tarefa atualizada
            tarefa_final = self.__tarefa_service.findById(id, usuario_id)
            
            return jsonify({
                "success": True,
                "message": f"Tarefa marcada como {novo_status} com sucesso!",
                "data": {
                    "tarefa": tarefa_final
                }
            }), 200
            
        except ErrorResponse as e:
            return jsonify({
                "success": False,
                "error": {
                    "message": e.message,
                    "details": e.details,
                    "code": e.status_code
                }
            }), e.status_code
        except Exception as e:
            print(f"❌ Erro inesperado em toggle_concluida: {traceback.format_exc()}")
            return jsonify({
                "success": False,
                "error": {
                    "message": "Erro interno no servidor",
                    "code": 500
                }
            }), 500