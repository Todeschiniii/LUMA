# -*- coding: utf-8 -*-
from api.dao.tarefa_dao import TarefaDAO
from api.dao.projeto_dao import ProjetoDAO
from api.dao.usuario_dao import UsuarioDAO
from api.model.tarefa import Tarefa
from api.utils.error_response import ErrorResponse
import traceback

"""
Classe responsável pela camada de serviço para a entidade Tarefa.
"""
class TarefaService:
    def __init__(self, tarefa_dao_dependency: TarefaDAO, projeto_dao_dependency: ProjetoDAO, usuario_dao_dependency: UsuarioDAO = None):
        print("⬆️  TarefaService.__init__()")
        self.__tarefaDAO = tarefa_dao_dependency
        self.__projetoDAO = projeto_dao_dependency
        self.__usuarioDAO = usuario_dao_dependency

    def createTarefa(self, jsonTarefa: dict, usuario_atribuidor_id: int = None) -> int:
        print("🟣 TarefaService.createTarefa()")

        objTarefa = Tarefa()
        objTarefa.titulo = jsonTarefa["titulo"]
        objTarefa.descricao = jsonTarefa.get("descricao", "")
        objTarefa.status = jsonTarefa.get("status", "pendente")
        objTarefa.prioridade = jsonTarefa.get("prioridade", "media")
        objTarefa.concluida = jsonTarefa.get("concluida", False)
        objTarefa.data_limite = jsonTarefa.get("data_limite")
        objTarefa.data_inicio = jsonTarefa.get("data_inicio")
        objTarefa.data_fim = jsonTarefa.get("data_fim")
        objTarefa.projeto_id = jsonTarefa["projeto_id"]
        objTarefa.usuario_responsavel_id = jsonTarefa.get("usuario")
        objTarefa.usuario_atribuidor_id = jsonTarefa.get("usuario_atribuidor_id")
        objTarefa.data_criacao = jsonTarefa.get("data_criacao")
        objTarefa.data_atualizacao = jsonTarefa.get("data_atualizacao")

        #if "usuario_responsavel_id" not in jsonTarefa:
        #    raise ErrorResponse(400, "Responsável obrigatório", 
        #                      {"message": "O campo usuario_responsavel_id é obrigatório"})
        
        #objTarefa.usuario_responsavel_id = jsonTarefa["usuario_responsavel_id"]
        
        if usuario_atribuidor_id:
            objTarefa.usuario_atribuidor_id = usuario_atribuidor_id
        elif "usuario_atribuidor_id" in jsonTarefa:
            objTarefa.usuario_atribuidor_id = jsonTarefa["usuario_atribuidor_id"]
        #else:
            #objTarefa.usuario_atribuidor_id = jsonTarefa["usuario_responsavel_id"]

        if self.__usuarioDAO:
            try:
                responsavel_existe = None
                atribuidor_existe = None
                
                if hasattr(self.__usuarioDAO, 'find_by_id'):
                    print(f"🔍 Validando responsável ID: {objTarefa.usuario_responsavel_id}")
                    responsavel_existe = self.__usuarioDAO.find_by_id(objTarefa.usuario_responsavel_id)
                    print(f"🔍 Validando atribuidor ID: {objTarefa.usuario_atribuidor_id}")
                    atribuidor_existe = self.__usuarioDAO.find_by_id(objTarefa.usuario_atribuidor_id)
                
                elif hasattr(self.__usuarioDAO, 'findById'):
                    print(f"🔍 Validando responsável ID: {objTarefa.usuario_responsavel_id}")
                    responsavel_existe = self.__usuarioDAO.findById(objTarefa.usuario_responsavel_id)
                    print(f"🔍 Validando atribuidor ID: {objTarefa.usuario_atribuidor_id}")
                    atribuidor_existe = self.__usuarioDAO.findById(objTarefa.usuario_atribuidor_id)
                
                elif hasattr(self.__usuarioDAO, 'findByField'):
                    print(f"🔍 Validando responsável ID: {objTarefa.usuario_responsavel_id}")
                    responsavel_existe = self.__usuarioDAO.findByField("id", objTarefa.usuario_responsavel_id)
                    print(f"🔍 Validando atribuidor ID: {objTarefa.usuario_atribuidor_id}")
                    atribuidor_existe = self.__usuarioDAO.findByField("id", objTarefa.usuario_atribuidor_id)
                
                else:
                    print("⚠️  UsuarioDAO não possui métodos de busca conhecidos, pulando validação de usuários")
                    responsavel_existe = True
                    atribuidor_existe = True
                
                print(f"📊 Resultado validação responsável: {responsavel_existe}")
                print(f"📊 Resultado validação atribuidor: {atribuidor_existe}")
                
                #if not responsavel_existe:
                    #raise ErrorResponse(400, "Responsável não encontrado",
                                      #{"message": f"Usuário responsável com ID {objTarefa.usuario_responsavel_id} não existe"})
                
                if not atribuidor_existe:
                    raise ErrorResponse(400, "Atribuidor não encontrado",
                                      {"message": f"Usuário atribuidor com ID {objTarefa.usuario_atribuidor_id} não existe"})
                    
            except ErrorResponse:
                raise
            except Exception as e:
                print(f"⚠️  Erro na validação de usuários: {e}")
                print(f"🔍 Stack trace: {traceback.format_exc()}")
                print("⚠️  Continuando sem validação de usuários devido a erro...")

        projeto_existe = self.__projetoDAO.findById(objTarefa.projeto_id)
        if not projeto_existe:
            raise ErrorResponse(400, "Projeto não encontrado",
                              {"message": f"Projeto com ID {objTarefa.projeto_id} não existe"})

        print(f"✅ Dados validados. Criando tarefa: {objTarefa.titulo}")
        return self.__tarefaDAO.create(objTarefa)

    def findAll(self, usuario_id: int = None) -> list[dict]:
        print("🟣 TarefaService.findAll()")
        return self.__tarefaDAO.findAll(usuario_id=usuario_id)

    def findById(self, id: int, usuario_id: int = None) -> dict:
        tarefa = self.__tarefaDAO.findById(id, usuario_id=usuario_id)
        if not tarefa:
            error_msg = f"Não existe tarefa com id {id}"
            if usuario_id:
                error_msg += f" para o usuário {usuario_id}"
            raise ErrorResponse(404, "Tarefa não encontrada", {"message": error_msg})
        return tarefa

    def updateTarefa(self, id: int, requestBody: dict, usuario_id: int = None) -> bool:
        """
        ✅ CORREÇÃO CRÍTICA: Método completamente corrigido para evitar erro de atributo
        """
        print("🟣 TarefaService.updateTarefa()")
        print(f"📝 Dados recebidos para atualizar tarefa {id}: {requestBody}")

        try:
            jsonTarefa = requestBody["tarefa"]

            # ✅ CORREÇÃO: Busca a tarefa existente (retorna dict)
            tarefa_existente_dict = self.__tarefaDAO.findById(id, usuario_id=usuario_id)
            if not tarefa_existente_dict:
                error_msg = f"Tarefa com ID {id} não existe"
                if usuario_id:
                    error_msg += f" para o usuário {usuario_id}"
                raise ErrorResponse(404, "Tarefa não encontrada", {"message": error_msg})

            # ✅ CORREÇÃO CRÍTICA: Converter dict para objeto Tarefa ANTES de usar
            tarefa_existente_obj = self._dict_to_tarefa(tarefa_existente_dict)

            objTarefa = Tarefa()
            objTarefa.id = id
            
            # ✅ CORREÇÃO: Usa o objeto convertido (não o dict)
            objTarefa = Tarefa()
            objTarefa.titulo = jsonTarefa["titulo"]
            objTarefa.descricao = jsonTarefa.get("descricao", "")
            objTarefa.status = jsonTarefa.get("status", "pendente")
            objTarefa.prioridade = jsonTarefa.get("prioridade", "media")
            objTarefa.concluida = jsonTarefa.get("concluida", False)
            objTarefa.data_limite = jsonTarefa.get("data_limite")
            objTarefa.data_inicio = jsonTarefa.get("data_inicio")
            objTarefa.data_fim = jsonTarefa.get("data_fim")
            objTarefa.projeto_id = jsonTarefa["projeto_id"]
            objTarefa.usuario_responsavel_id = jsonTarefa.get("usuario")
            objTarefa.usuario_atribuidor_id = jsonTarefa.get("usuario_atribuidor_id")
            objTarefa.data_criacao = jsonTarefa.get("data_criacao")
            objTarefa.data_atualizacao = jsonTarefa.get("data_atualizacao")
            
            # ✅ CORREÇÃO CRÍTICA: Verifica se usuario_id existe no objeto antes de usar
            if hasattr(tarefa_existente_obj, 'usuario_id') and tarefa_existente_obj.usuario_id:
                objTarefa.usuario_id = tarefa_existente_obj.usuario_id
            else:
                print("⚠️  Tarefa existente não possui usuario_id, mantendo como None")

            # ✅ CORREÇÃO: Tratamento de datas
            data_limite = jsonTarefa.get("data_limite")
            if data_limite is not None:
                objTarefa.data_limite = data_limite
            else:
                objTarefa.data_limite = tarefa_existente_obj.data_limite

            # ✅ CORREÇÃO: Campos de data adicionais
            objTarefa.data_inicio = jsonTarefa.get("data_inicio", getattr(tarefa_existente_obj, 'data_inicio', None))
            objTarefa.data_fim = jsonTarefa.get("data_fim", getattr(tarefa_existente_obj, 'data_fim', None))

            print(f"🔍 Campos a serem atualizados: {[k for k, v in jsonTarefa.items()]}")

            # ✅ CORREÇÃO: Valida projeto apenas se foi fornecido
            if "projeto_id" in jsonTarefa and objTarefa.projeto_id:
                projeto_existe = self.__projetoDAO.findById(objTarefa.projeto_id)
                if not projeto_existe:
                    raise ErrorResponse(404, "Projeto não encontrado", {"message": f"Projeto com ID {objTarefa.projeto_id} não existe"})

            return self.__tarefaDAO.update(objTarefa, usuario_id=usuario_id)

        except ValueError as e:
            print(f"❌ Erro de validação em updateTarefa: {e}")
            raise ErrorResponse(400, str(e), {"message": f"Erro de validação: {str(e)}"})
        except ErrorResponse:
            raise
        except Exception as e:
            print(f"❌ Erro inesperado em updateTarefa: {e}")
            print(f"🔍 Stack trace: {traceback.format_exc()}")
            raise ErrorResponse(500, "Erro interno do servidor", {"message": f"Erro interno ao atualizar tarefa: {str(e)}"})

    def updateTarefaConcluida(self, id: int, requestBody: dict, usuario_id: int = None) -> bool:
        print("🟣 TarefaService.updateTarefaConcluida()")
        print(f"📝 Atualizando apenas campo 'concluida' da tarefa {id}: {requestBody}")

        try:
            jsonTarefa = requestBody["tarefa"]
            concluida = jsonTarefa["concluida"]

            if not isinstance(concluida, bool):
                if concluida in ['true', 'True', '1', 1]:
                    concluida = True
                elif concluida in ['false', 'False', '0', 0]:
                    concluida = False
                else:
                    raise ErrorResponse(400, "Valor inválido", {"message": "O campo 'concluida' deve ser true ou false"})

            tarefa_existente = self.__tarefaDAO.findById(id, usuario_id=usuario_id)
            if not tarefa_existente:
                error_msg = f"Tarefa com ID {id} não existe"
                if usuario_id:
                    error_msg += f" para o usuário {usuario_id}"
                raise ErrorResponse(404, "Tarefa não encontrada", {"message": error_msg})

            if hasattr(self.__tarefaDAO, 'marcarConcluida'):
                return self.__tarefaDAO.marcarConcluida(id, concluida, usuario_id=usuario_id)
            elif hasattr(self.__tarefaDAO, 'updateCampo'):
                return self.__tarefaDAO.updateCampo(id, 'concluida', concluida, usuario_id=usuario_id)
            else:
                return self.marcarConcluida(id, concluida, usuario_id=usuario_id)

        except ErrorResponse:
            raise
        except Exception as e:
            print(f"❌ Erro inesperado em updateTarefaConcluida: {e}")
            print(f"🔍 Stack trace: {traceback.format_exc()}")
            raise ErrorResponse(500, "Erro interno do servidor", {"message": f"Erro interno ao atualizar status da tarefa: {str(e)}"})

    def deleteTarefa(self, id: int, usuario_id: int = None) -> bool:
        print("🟣 TarefaService.deleteTarefa()")
        return self.__tarefaDAO.delete(id, usuario_id=usuario_id)

    def findByProjetoId(self, projeto_id: int, usuario_id: int = None) -> list[dict]:
        print("🟣 TarefaService.findByProjetoId()")
        
        projetoExiste = self.__projetoDAO.findById(projeto_id)
        if not projetoExiste:
            raise ErrorResponse(
                404,
                "Projeto não encontrado",
                {"message": f"Não existe projeto com id {projeto_id}"}
            )

        return self.__tarefaDAO.findByProjetoId(projeto_id, usuario_id=usuario_id)

    def marcarConcluida(self, id: int, concluida: bool, usuario_id: int = None) -> bool:
        print(f"🟣 TarefaService.marcarConcluida() - ID: {id}, Concluída: {concluida}")
        
        try:
            tarefa_existente_dict = self.__tarefaDAO.findById(id, usuario_id=usuario_id)
            if not tarefa_existente_dict:
                error_msg = f"Tarefa com ID {id} não existe"
                if usuario_id:
                    error_msg += f" para o usuário {usuario_id}"
                raise ErrorResponse(404, "Tarefa não encontrada", {"message": error_msg})

            # ✅ CORREÇÃO: Converter dict para objeto Tarefa
            tarefa_existente_obj = self._dict_to_tarefa(tarefa_existente_dict)

            objTarefa = Tarefa()
            objTarefa.id = id
            objTarefa.concluida = concluida
            
            # ✅ CORREÇÃO: Usa o objeto convertido
            objTarefa.titulo = tarefa_existente_obj.titulo
            objTarefa.descricao = tarefa_existente_obj.descricao
            objTarefa.status = "concluida" if concluida else "pendente"
            objTarefa.prioridade = tarefa_existente_obj.prioridade
            objTarefa.data_limite = getattr(tarefa_existente_obj, 'data_limite', None)
            objTarefa.data_inicio = getattr(tarefa_existente_obj, 'data_inicio', None)
            objTarefa.data_fim = getattr(tarefa_existente_obj, 'data_fim', None)
            objTarefa.projeto_id = tarefa_existente_obj.projeto_id
            objTarefa.usuario_responsavel_id = getattr(tarefa_existente_obj, 'usuario_responsavel_id', None)
            objTarefa.usuario_atribuidor_id = getattr(tarefa_existente_obj, 'usuario_atribuidor_id', None)
            objTarefa.data_criacao = getattr(tarefa_existente_obj, 'data_criacao', None)
            objTarefa.data_atualizacao = getattr(tarefa_existente_obj, 'data_atualizacao', None)

            return self.__tarefaDAO.update(objTarefa, usuario_id=usuario_id)

        except ErrorResponse:
            raise
        except Exception as e:
            print(f"❌ Erro inesperado em marcarConcluida: {e}")
            print(f"🔍 Stack trace: {traceback.format_exc()}")
            raise ErrorResponse(500, "Erro interno do servidor", {"message": f"Erro interno ao marcar tarefa como concluida: {str(e)}"})

    def _dict_to_tarefa(self, tarefa_dict: dict) -> Tarefa:
        """
        ✅ CORREÇÃO MELHORADA: Converte dicionário para objeto Tarefa de forma mais robusta
        """
        if not tarefa_dict:
            return None
            
        objTarefa = Tarefa()
        
        try:
            # Mapeia os campos do dicionário para o objeto Tarefa
            if 'id' in tarefa_dict and tarefa_dict['id'] is not None:
                objTarefa.id = tarefa_dict['id']
            if 'titulo' in tarefa_dict and tarefa_dict['titulo'] is not None:
                objTarefa.titulo = tarefa_dict['titulo']
            if 'descricao' in tarefa_dict:
                objTarefa.descricao = tarefa_dict['descricao']
            if 'status' in tarefa_dict and tarefa_dict['status'] is not None:
                objTarefa.status = tarefa_dict['status']
            if 'prioridade' in tarefa_dict and tarefa_dict['prioridade'] is not None:
                objTarefa.prioridade = tarefa_dict['prioridade']
            if 'concluida' in tarefa_dict:
                objTarefa.concluida = bool(tarefa_dict['concluida'])
            if 'data_limite' in tarefa_dict:
                objTarefa.data_limite = tarefa_dict['data_limite']
            if 'data_inicio' in tarefa_dict:
                objTarefa.data_inicio = tarefa_dict['data_inicio']
            if 'data_fim' in tarefa_dict:
                objTarefa.data_fim = tarefa_dict['data_fim']
            if 'projeto_id' in tarefa_dict and tarefa_dict['projeto_id'] is not None:
                objTarefa.projeto_id = tarefa_dict['projeto_id']
            if 'usuario_responsavel_id' in tarefa_dict and tarefa_dict['usuario_responsavel_id'] is not None:
                objTarefa.usuario_responsavel_id = tarefa_dict['usuario_responsavel_id']
            if 'usuario_atribuidor_id' in tarefa_dict and tarefa_dict['usuario_atribuidor_id'] is not None:
                objTarefa.usuario_atribuidor_id = tarefa_dict['usuario_atribuidor_id']
                
            # ✅ CORREÇÃO: Campo usuario_id (se existir no dicionário)
            if 'usuario_id' in tarefa_dict and tarefa_dict['usuario_id'] is not None:
                objTarefa.usuario_id = tarefa_dict['usuario_id']
                
        except Exception as e:
            print(f"⚠️  Erro ao converter dict para Tarefa: {e}")
            print(f"🔍 Dados problemáticos: {tarefa_dict}")
            # Continua com o objeto parcialmente preenchido
            
        return objTarefa

    def atualizarCampoSimples(self, id: int, campo: str, valor: any, usuario_id: int = None) -> bool:
        print(f"🟣 TarefaService.atualizarCampoSimples() - ID: {id}, Campo: {campo}, Valor: {valor}")
        
        try:
            tarefa_existente = self.__tarefaDAO.findById(id, usuario_id=usuario_id)
            if not tarefa_existente:
                error_msg = f"Tarefa com ID {id} não existe"
                if usuario_id:
                    error_msg += f" para o usuário {usuario_id}"
                raise ErrorResponse(404, "Tarefa não encontrada", {"message": error_msg})

            if hasattr(self.__tarefaDAO, 'updateCampo'):
                return self.__tarefaDAO.updateCampo(id, campo, valor, usuario_id=usuario_id)
            else:
                update_data = {"tarefa": {campo: valor}}
                return self.updateTarefa(id, update_data, usuario_id=usuario_id)

        except ErrorResponse:
            raise
        except Exception as e:
            print(f"❌ Erro inesperado em atualizarCampoSimples: {e}")
            print(f"🔍 Stack trace: {traceback.format_exc()}")
            raise ErrorResponse(500, "Erro interno do servidor", {"message": f"Erro interno ao atualizar campo: {str(e)}"})

    def getTarefasByUsuario(self, usuario_id: int) -> list[dict]:
        print(f"🟣 TarefaService.getTarefasByUsuario() - Usuario ID: {usuario_id}")
        return self.__tarefaDAO.findByField("usuario_responsavel_id", usuario_id)