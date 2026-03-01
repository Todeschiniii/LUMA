# -*- coding: utf-8 -*-
from datetime import datetime, date

class Projeto:
    def __init__(self):
        """
        Inicializa todos os atributos como atributos de instância.
        """
        self.__id = None
        self.__nome = None
        self.__descricao = None
        self.__data_inicio = None
        self.__data_fim = None  
        self.__data_limite = None
        self.__status = None
        self.__usuario_id = None
        self.__data_criacao = None
        self.__data_atualizacao = None

    @property
    def id(self):
        """
        Getter para id
        :return: int - Identificador único do projeto
        """
        return self.__id

    @id.setter
    def id(self, value):
        """
        Define o ID do projeto.

        🔹 Regra de domínio: garante que o ID seja sempre um número inteiro positivo.

        :param value: int - Número inteiro positivo representando o ID do projeto.
        :raises ValueError: Lança erro se o valor não for número, não for inteiro ou for menor/igual a zero.

        Exemplo:
        >>> projeto = Projeto()
        >>> projeto.id = 1   # ✅ válido
        >>> projeto.id = -5  # ❌ lança erro
        >>> projeto.id = 0   # ❌ lança erro
        >>> projeto.id = 3.14  # ❌ lança erro
        >>> projeto.id = None  # ❌ lança erro
        """
        if value is None:
            self.__id = None
            return
            
        try:
            parsed = int(value)
        except (ValueError, TypeError):
            raise ValueError("id deve ser um número inteiro.")

        if parsed <= 0:
            raise ValueError("id deve ser maior que zero.")

        self.__id = parsed

    @property
    def nome(self):
        """
        Getter para nome
        :return: str - Nome do projeto
        """
        return self.__nome

    @nome.setter
    def nome(self, value):
        """
        Define o nome do projeto.

        🔹 Regra de domínio: garante que o nome seja sempre uma string não vazia
        e com pelo menos 3 caracteres.

        :param value: str - Nome do projeto.
        :raises ValueError: Lança erro se o valor não for string, estiver vazio, tiver menos de 3 caracteres ou for None.

        Exemplo:
        >>> projeto = Projeto()
        >>> projeto.nome = "API de E-commerce"   # ✅ válido
        >>> projeto.nome = "AB"                  # ❌ lança erro
        >>> projeto.nome = ""                    # ❌ lança erro
        >>> projeto.nome = None                  # ❌ lança erro
        """
        if value is None:
            raise ValueError("nome não pode ser None.")

        if not isinstance(value, str):
            raise ValueError("nome deve ser uma string.")

        nome = value.strip()
        if len(nome) < 3:
            raise ValueError("nome deve ter pelo menos 3 caracteres.")

        self.__nome = nome

    @property
    def descricao(self):
        """
        Getter para descricao
        :return: str - Descrição do projeto
        """
        return self.__descricao

    @descricao.setter
    def descricao(self, value):
        """
        Define a descrição do projeto.

        🔹 Regra de domínio: garante que a descrição seja uma string.

        :param value: str - Descrição do projeto.
        :raises ValueError: Lança erro se o valor não for string.

        Exemplo:
        >>> projeto = Projeto()
        >>> projeto.descricao = "Desenvolver a API REST"   # ✅ válido
        >>> projeto.descricao = None                       # ✅ válido (None é permitido)
        >>> projeto.descricao = 123                        # ❌ lança erro
        """
        if value is not None and not isinstance(value, str):
            raise ValueError("descricao deve ser uma string ou None.")

        self.__descricao = value

    @property
    def data_inicio(self):
        """
        Getter para data_inicio
        :return: date - Data de início do projeto
        """
        return self.__data_inicio

    @data_inicio.setter
    def data_inicio(self, value):
        """
        Define a data de início do projeto.

        🔹 Regra de domínio: garante que a data seja um objeto date ou string no formato YYYY-MM-DD.

        :param value: date ou str - Data de início do projeto.
        :raises ValueError: Lança erro se o valor não for date ou string no formato correto.

        Exemplo:
        >>> projeto = Projeto()
        >>> from datetime import date
        >>> projeto.data_inicio = date(2025, 11, 1)   # ✅ válido
        >>> projeto.data_inicio = "2025-11-01"        # ✅ válido (agora aceita string)
        >>> projeto.data_inicio = None                # ✅ válido (None é permitido)
        >>> projeto.data_inicio = "01/11/2025"        # ❌ lança erro (formato inválido)
        """
        if value is None:
            self.__data_inicio = None
            return

        # ✅ CORREÇÃO: Aceita tanto date quanto string
        if isinstance(value, date):
            self.__data_inicio = value
        elif isinstance(value, str):
            try:
                # Tenta converter string para date
                self.__data_inicio = datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("data_inicio deve ser um objeto date, string no formato YYYY-MM-DD ou None.")
        else:
            raise ValueError("data_inicio deve ser um objeto date, string no formato YYYY-MM-DD ou None.")

    @property
    def data_fim(self):
        """
        Getter para data_fim
        :return: date - Data de término do projeto
        """
        return self.__data_fim

    @data_fim.setter
    def data_fim(self, value):
        """
        Define a data de término do projeto.

        🔹 Regra de domínio: garante que a data seja um objeto date ou string no formato YYYY-MM-DD.

        :param value: date ou str - Data de término do projeto.
        :raises ValueError: Lança erro se o valor não for date ou string no formato correto.

        Exemplo:
        >>> projeto = Projeto()
        >>> from datetime import date
        >>> projeto.data_fim = date(2025, 12, 1)   # ✅ válido
        >>> projeto.data_fim = "2025-12-01"        # ✅ válido (agora aceita string)
        >>> projeto.data_fim = None                # ✅ válido (None é permitido)
        >>> projeto.data_fim = "01/12/2025"        # ❌ lança erro (formato inválido)
        """
        if value is None:
            self.__data_fim = None
            return

        # ✅ CORREÇÃO: Aceita tanto date quanto string
        if isinstance(value, date):
            self.__data_fim = value
        elif isinstance(value, str):
            try:
                # Tenta converter string para date
                self.__data_fim = datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("data_fim deve ser um objeto date, string no formato YYYY-MM-DD ou None.")
        else:
            raise ValueError("data_fim deve ser um objeto date, string no formato YYYY-MM-DD ou None.")

    @property
    def status(self):
        """
        Getter para status
        :return: str - Status do projeto
        """
        return self.__status

    @status.setter
    def status(self, value):
        """
        Define o status do projeto.

        🔹 Regra de domínio: garante que o status seja um dos valores permitidos.

        :param value: str - Status do projeto.
        :raises ValueError: Lança erro se o valor não for um status válido.

        Exemplo:
        >>> projeto = Projeto()
        >>> projeto.status = "pendente"       # ✅ válido
        >>> projeto.status = "andamento"      # ✅ válido  
        >>> projeto.status = "concluido"      # ✅ válido
        >>> projeto.status = "Inválido"       # ❌ lança erro
        >>> projeto.status = None             # ❌ lança erro
        """
        if value is None:
            raise ValueError("status não pode ser None.")

        if not isinstance(value, str):
            raise ValueError("status deve ser uma string.")

        # ✅ CORREÇÃO: Status compatíveis com o frontend
        status_validos = ["pendente", "andamento", "concluido"]
        if value not in status_validos:
            raise ValueError(f"status deve ser um dos valores: {', '.join(status_validos)}")

        self.__status = value

    @property
    def usuario_id(self):
        """
        Getter para usuario_id
        :return: int - ID do usuário proprietário do projeto
        """
        return self.__usuario_id

    @usuario_id.setter
    def usuario_id(self, value):
        """
        Define o ID do usuário proprietário do projeto.

        🔹 Regra de domínio: garante que o ID do usuário seja sempre um número inteiro positivo.

        :param value: int - Número inteiro positivo representando o ID do usuário.
        :raises ValueError: Lança erro se o valor não for número, não for inteiro ou for menor/igual a zero.

        Exemplo:
        >>> projeto = Projeto()
        >>> projeto.usuario_id = 1   # ✅ válido
        >>> projeto.usuario_id = -5  # ❌ lança erro
        >>> projeto.usuario_id = 0   # ❌ lança erro
        >>> projeto.usuario_id = 3.14  # ❌ lança erro
        >>> projeto.usuario_id = None  # ✅ válido (None é permitido)
        """
        if value is None:
            self.__usuario_id = None
            return
            
        try:
            parsed = int(value)
        except (ValueError, TypeError):
            raise ValueError("usuario_id deve ser um número inteiro.")

        if parsed <= 0:
            raise ValueError("usuario_id deve ser maior que zero.")

        self.__usuario_id = parsed

    # Propriedade data_limite (igual ao Código 1)
    @property
    def data_limite(self):
        return self.__data_limite

    @data_limite.setter
    def data_limite(self, value):
        if value is None:
            self.__data_limite = None
            return

        if isinstance(value, date):
            self.__data_limite = value
        elif isinstance(value, str):
            try:
                self.__data_limite = datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("data_limite deve ser um objeto date, string no formato YYYY-MM-DD ou None.")
        else:
            raise ValueError("data_limite deve ser um objeto date, string no formato YYYY-MM-DD ou None.")

    # Propriedade data_criacao (igual ao Código 2)
    @property
    def data_criacao(self):
        return self.__data_criacao

    @data_criacao.setter
    def data_criacao(self, value):
        if value is None:
            self.__data_criacao = datetime.now()
            return

        if isinstance(value, datetime):
            self.__data_criacao = value
        elif isinstance(value, str):
            try:
                self.__data_criacao = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                raise ValueError("data_criacao deve ser um objeto datetime ou string no formato YYYY-MM-DD HH:MM:SS.")
        else:
            raise ValueError("data_criacao deve ser um objeto datetime ou string no formato YYYY-MM-DD HH:MM:SS.")

    # Nova propriedade: data_atualizacao
    @property
    def data_atualizacao(self):
        """
        Getter para data_atualizacao
        :return: datetime - Data da última atualização do projeto
        """
        return self.__data_atualizacao

    @data_atualizacao.setter
    def data_atualizacao(self, value):
        """
        Define a data da última atualização do projeto.

        :param value: datetime ou str - Data da última atualização do projeto.
        :raises ValueError: Lança erro se o valor não for datetime ou string no formato correto.
        """
        if value is None:
            self.__data_atualizacao = datetime.now()
            return

        if isinstance(value, datetime):
            self.__data_atualizacao = value
        elif isinstance(value, str):
            try:
                self.__data_atualizacao = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                raise ValueError("data_atualizacao deve ser um objeto datetime ou string no formato YYYY-MM-DD HH:MM:SS.")
        else:
            raise ValueError("data_atualizacao deve ser um objeto datetime ou string no formato YYYY-MM-DD HH:MM:SS.")

    def to_dict(self):
        """
        Converte o objeto Projeto para dicionário.
        
        :return: dict - Representação em dicionário do projeto
        """
        return {
            "id": self.__id,
            "nome": self.__nome,
            "descricao": self.__descricao,
            "data_inicio": self.__data_inicio.isoformat() if self.__data_inicio else None,
            "data_fim": self.__data_fim.isoformat() if self.__data_fim else None,
            "data_limite": self.__data_limite.isoformat() if self.__data_limite else None,
            "status": self.__status,
            "usuario_id": self.__usuario_id,
            "data_criacao": self.__data_criacao.isoformat() if self.__data_criacao else None,
            "data_atualizacao": self.__data_atualizacao.isoformat() if self.__data_atualizacao else None
        }

    def __str__(self):
        """
        Representação em string do objeto Projeto.
        """
        return f"Projeto(id={self.__id}, nome='{self.__nome}', status='{self.__status}')"

    def __repr__(self):
        """
        Representação oficial do objeto Projeto.
        """
        return self.__str__()