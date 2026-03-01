# dao/usuario_dao.py
from datetime import datetime
from api.model.usuario import Usuario

class UsuarioDAO:
    def __init__(self, database_dependency):
        print("⬆️  UsuarioDAO.__init__()")
        self.__database = database_dependency
        self._create_tables()

    def _create_tables(self):
        """Cria as tabelas necessárias se não existirem"""
        print("🟢 UsuarioDAO._create_tables()")
        try:
            SQL = '''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    nome VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    senha_hash VARCHAR(255) NOT NULL,
                    empresa VARCHAR(255) NULL,
                    perfil_tipo VARCHAR(20) DEFAULT 'pessoal', -- 'pessoal' ou 'empresa'
                    hierarquia VARCHAR(20) DEFAULT 'pessoal', -- 'adm', 'gerente', 'funcionario', 'pessoal'
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            '''
            self.__database.execute_query(SQL)
            print("✅ Tabela 'usuarios' criada/verificada com sucesso!")
        except Exception as e:
            print(f"❌ Erro em UsuarioDAO._create_tables(): {e}")

    def email_exists(self, email: str) -> bool:
        """
        Verifica se um email já existe no banco
        :param email: Email a verificar
        :return: Boolean indicando se existe
        """
        print(f"🟢 UsuarioDAO.email_exists() - Email: {email}")
        try:
            SQL = "SELECT id FROM usuarios WHERE email = %s"
            result = self.__database.execute_query(SQL, (email,), fetch=True)
            return len(result) > 0
        except Exception as e:
            print(f"❌ Erro em UsuarioDAO.email_exists(): {e}")
            raise

    def create(self, usuario: Usuario) -> int:
        """
        Cria um novo usuário no banco de dados
        :param usuario: Objeto Usuario
        :return: ID do usuário criado
        """
        print("🟢 UsuarioDAO.create()")
        try:
            SQL = '''
                INSERT INTO usuarios (nome, email, senha_hash, empresa, perfil_tipo, hierarquia, data_criacao, data_atualizacao)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            '''
            params = (
                usuario.nome, 
                usuario.email, 
                usuario.senha_hash, 
                usuario.empresa,
                usuario.perfil_tipo,
                usuario.hierarquia,
                usuario.data_criacao,
                usuario.data_atualizacao
            )

            insert_id = self.__database.execute_query(SQL, params)
            
            if not insert_id:
                raise Exception("Falha ao inserir usuário")
            return insert_id

        except Exception as e:
            if "Duplicate entry" in str(e) or "UNIQUE constraint" in str(e):
                raise ValueError("Email já cadastrado")
            print(f"❌ Erro em UsuarioDAO.create(): {e}")
            raise
    
    def buscar_por_email(self, email):
        """
        Busca um usuário pelo email
        """
        try:
            query = "SELECT * FROM usuarios WHERE email = %s"
            result = self.__database.execute_query(query, (email,), fetch=True)
            
            if result and len(result) > 0:
                return result[0]
            return None
            
        except Exception as e:
            print(f"❌ Erro ao buscar usuário por email: {e}")
            return None

    def buscar_por_id(self, usuario_id):
        """
        Busca um usuário pelo ID
        """
        try:
            query = "SELECT * FROM usuarios WHERE id = %s"
            result = self.__database.execute_query(query, (usuario_id,), fetch=True)
            
            if result and len(result) > 0:
                return result[0]
            return None
            
        except Exception as e:
            print(f"❌ Erro ao buscar usuário por ID: {e}")
            return None

    def atualizar_senha(self, usuario_id, senha_hash):
        """
        Atualiza a senha de um usuário
        """
        try:
            query = "UPDATE usuarios SET senha_hash = %s WHERE id = %s"
            result = self.__database.execute_query(query, (senha_hash, usuario_id))
            return result > 0
            
        except Exception as e:
            print(f"❌ Erro ao atualizar senha: {e}")
            return False
    
    def find_by_id(self, usuario_id: int) -> Usuario | None:
        """
        Busca usuário por ID
        :param usuario_id: ID do usuário
        :return: Objeto Usuario ou None
        """
        print(f"✅ UsuarioDAO.find_by_id() - ID: {usuario_id}")
        try:
            SQL = '''
                SELECT id, nome, email, senha_hash, empresa, perfil_tipo, hierarquia, data_criacao, data_atualizacao
                FROM usuarios WHERE id = %s
            '''
            rows = self.__database.execute_query(SQL, (usuario_id,), fetch=True)

            if not rows:
                return None

            row = rows[0]
            usuario = Usuario()
            usuario.id = row["id"]
            usuario.nome = row["nome"]
            usuario.email = row["email"]
            usuario.senha_hash = row["senha_hash"]
            
            # ✅ CORREÇÃO: Verifica se a coluna empresa existe antes de acessar
            usuario.empresa = row.get("empresa")  # Usa get() para evitar KeyError

            usuario.perfil_tipo = row["perfil_tipo"]
            usuario.hierarquia = row["hierarquia"]

            # Tratamento para datas
            if row["data_criacao"]:
                if hasattr(row["data_criacao"], 'isoformat'):
                    usuario.data_criacao = row["data_criacao"]
                else:
                    try:
                        usuario.data_criacao = datetime.strptime(str(row["data_criacao"]), '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        usuario.data_criacao = datetime.strptime(str(row["data_criacao"]), '%Y-%m-%d %H:%M:%S.%f')
            
            if row["data_atualizacao"]:
                if hasattr(row["data_atualizacao"], 'isoformat'):
                    usuario.data_atualizacao = row["data_atualizacao"]
                else:
                    try:
                        usuario.data_atualizacao = datetime.strptime(str(row["data_atualizacao"]), '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        usuario.data_atualizacao = datetime.strptime(str(row["data_atualizacao"]), '%Y-%m-%d %H:%M:%S.%f')
            
            return usuario

        except Exception as e:
            print(f"❌ Erro em UsuarioDAO.find_by_id(): {e}")
            raise

    def find_by_email(self, email: str) -> Usuario | None:
        """
        Busca usuário por email
        :param email: Email do usuário
        :return: Objeto Usuario ou None
        """
        print(f"🟢 UsuarioDAO.find_by_email() - Email: {email}")
        try:
            SQL = '''
                SELECT id, nome, email, senha_hash, empresa, perfil_tipo, hierarquia, data_criacao, data_atualizacao
                FROM usuarios WHERE email = %s
            '''
            rows = self.__database.execute_query(SQL, (email,), fetch=True)

            if not rows:
                return None

            row = rows[0]
            usuario = Usuario()
            usuario.id = row["id"]
            usuario.nome = row["nome"]
            usuario.email = row["email"]
            usuario.senha_hash = row["senha_hash"]
            
            # ✅ CORREÇÃO: Verifica se a coluna empresa existe antes de acessar
            usuario.empresa = row.get("empresa")  # Usa get() para evitar KeyError
            
            usuario.perfil_tipo = row["perfil_tipo"]
            usuario.hierarquia = row["hierarquia"]

            # Tratamento para datas
            if row["data_criacao"]:
                if hasattr(row["data_criacao"], 'isoformat'):
                    usuario.data_criacao = row["data_criacao"]
                else:
                    try:
                        usuario.data_criacao = datetime.strptime(str(row["data_criacao"]), '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        usuario.data_criacao = datetime.strptime(str(row["data_criacao"]), '%Y-%m-%d %H:%M:%S.%f')
            
            if row["data_atualizacao"]:
                if hasattr(row["data_atualizacao"], 'isoformat'):
                    usuario.data_atualizacao = row["data_atualizacao"]
                else:
                    try:
                        usuario.data_atualizacao = datetime.strptime(str(row["data_atualizacao"]), '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        usuario.data_atualizacao = datetime.strptime(str(row["data_atualizacao"]), '%Y-%m-%d %H:%M:%S.%f')
            
            return usuario

        except Exception as e:
            print(f"❌ Erro em UsuarioDAO.find_by_email(): {e}")
            raise

    def find_all(self) -> list[Usuario]:
        """
        Retorna todos os usuários
        :return: Lista de objetos Usuario
        """
        print("🟢 UsuarioDAO.find_all()")
        try:
            SQL = '''
                SELECT id, nome, email, senha_hash, empresa, perfil_tipo, hierarquia, data_criacao, data_atualizacao
                FROM usuarios ORDER BY nome
            '''
            rows = self.__database.execute_query(SQL, fetch=True)

            usuarios = []
            for row in rows:
                usuario = Usuario()
                usuario.id = row["id"]
                usuario.nome = row["nome"]
                usuario.email = row["email"]
                usuario.senha_hash = row["senha_hash"]
                
                # ✅ CORREÇÃO PRINCIPAL: Usa get() para evitar KeyError
                usuario.empresa = row.get("empresa")  # Isso evita o erro se a coluna não existir
                
                usuario.perfil_tipo = row["perfil_tipo"]
                usuario.hierarquia = row["hierarquia"]

                # Tratamento para datas
                if row["data_criacao"]:
                    if hasattr(row["data_criacao"], 'isoformat'):
                        usuario.data_criacao = row["data_criacao"]
                    else:
                        try:
                            usuario.data_criacao = datetime.strptime(str(row["data_criacao"]), '%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            usuario.data_criacao = datetime.strptime(str(row["data_criacao"]), '%Y-%m-%d %H:%M:%S.%f')
                
                if row["data_atualizacao"]:
                    if hasattr(row["data_atualizacao"], 'isoformat'):
                        usuario.data_atualizacao = row["data_atualizacao"]
                    else:
                        try:
                            usuario.data_atualizacao = datetime.strptime(str(row["data_atualizacao"]), '%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            usuario.data_atualizacao = datetime.strptime(str(row["data_atualizacao"]), '%Y-%m-%d %H:%M:%S.%f')
                
                usuarios.append(usuario)

            print(f"✅ UsuarioDAO.find_all() encontrou {len(usuarios)} usuários")
            return usuarios

        except Exception as e:
            print(f"❌ Erro em UsuarioDAO.find_all(): {e}")
            raise

    def update(self, usuario: Usuario) -> bool:
        """
        Atualiza usuário
        :param usuario: Objeto Usuario
        :return: Boolean indicando sucesso
        """
        print(f"🟢 UsuarioDAO.update() - ID: {usuario.id}")
        try:
            SQL = '''
                UPDATE usuarios 
                SET nome = %s, email = %s, senha_hash = %s, empresa = %s, perfil_tipo = %s, hierarquia = %s, data_criacao = %s, data_atualizacao = %s
                WHERE id = %s
            '''
            params = (
                usuario.nome, 
                usuario.email, 
                usuario.senha_hash, 
                usuario.empresa,
                usuario.perfil_tipo,
                usuario.hierarquia,
                usuario.data_criacao,
                usuario.data_atualizacao,
                usuario.id
            )

            affected = self.__database.execute_query(SQL, params)
            return affected > 0

        except Exception as e:
            if "Duplicate entry" in str(e) or "UNIQUE constraint" in str(e):
                raise ValueError("Email já cadastrado")
            print(f"❌ Erro em UsuarioDAO.update(): {e}")
            raise

    def delete(self, usuario_id: int) -> bool:
        """
        Exclui usuário por ID
        :param usuario_id: ID do usuário
        :return: Boolean indicando sucesso
        """
        print(f"🟢 UsuarioDAO.delete() - ID: {usuario_id}")
        try:
            SQL = 'DELETE FROM usuarios WHERE id = %s'
            affected = self.__database.execute_query(SQL, (usuario_id,))
            return affected > 0

        except Exception as e:
            print(f"❌ Erro em UsuarioDAO.delete(): {e}")
            raise