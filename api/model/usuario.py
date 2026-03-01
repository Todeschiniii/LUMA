# models/usuario.py
from datetime import datetime

class Usuario:
    def __init__(self):
        """
        Inicializa todos os atributos como atributos de instância.
        """
        self.__id = None
        self.__nome = None
        self.__email = None
        self.__senha_hash = None
        self.__empresa = None
        self.__perfil_tipo = None
        self.__hierarquia = None
        self.__data_atualizacao = None
        self.__data_atualizacao = None

    @property
    def id(self):
        """
        Getter para id
        :return: int - Identificador único do usuário
        """
        return self.__id

    @id.setter
    def id(self, value):
        """
        Define o ID do usuário.

        🔹 Regra de domínio: garante que o ID seja sempre um número inteiro positivo.

        :param value: int - Número inteiro positivo representando o ID do usuário.
        :raises ValueError: Lança erro se o valor não for número, não for inteiro ou for menor/igual a zero.

        Exemplo:
        >>> usuario = Usuario()
        >>> usuario.id = 1   # ✅ válido
        >>> usuario.id = -5  # ❌ lança erro
        >>> usuario.id = 0   # ❌ lança erro
        >>> usuario.id = 3.14  # ❌ lança erro
        >>> usuario.id = None  # ❌ lança erro
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
        :return: str - Nome do usuário
        """
        return self.__nome

    @nome.setter
    def nome(self, value):
        """
        Define o nome do usuário.

        🔹 Regra de domínio: garante que o nome seja sempre uma string não vazia
        e com pelo menos 2 caracteres.

        :param value: str - Nome do usuário.
        :raises ValueError: Lança erro se o valor não for string, estiver vazio, tiver menos de 2 caracteres ou for None.

        Exemplo:
        >>> usuario = Usuario()
        >>> usuario.nome = "Ana Silva"   # ✅ válido
        >>> usuario.nome = "A"           # ❌ lança erro
        >>> usuario.nome = ""            # ❌ lança erro
        >>> usuario.nome = None          # ❌ lança erro
        """
        if value is None:
            raise ValueError("nome não pode ser None.")

        if not isinstance(value, str):
            raise ValueError("nome deve ser uma string.")

        nome = value.strip()
        if len(nome) < 2:
            raise ValueError("nome deve ter pelo menos 2 caracteres.")

        self.__nome = nome

    @property
    def email(self):
        """
        Getter para email
        :return: str - Email do usuário
        """
        return self.__email

    @email.setter
    def email(self, value):
        """
        Define o email do usuário.

        🔹 Regra de domínio: garante que o email seja sempre uma string válida
        contendo o caractere '@'.

        :param value: str - Email do usuário.
        :raises ValueError: Lança erro se o valor não for string, não conter '@' ou for None.

        Exemplo:
        >>> usuario = Usuario()
        >>> usuario.email = "ana@email.com"   # ✅ válido
        >>> usuario.email = "ana.email.com"   # ❌ lança erro
        >>> usuario.email = ""                # ❌ lança erro
        >>> usuario.email = None              # ❌ lança erro
        """
        if value is None:
            raise ValueError("email não pode ser None.")

        if not isinstance(value, str):
            raise ValueError("email deve ser uma string.")

        email = value.strip()
        if len(email) == 0:
            raise ValueError("email não pode estar vazio.")

        if '@' not in email:
            raise ValueError("email deve conter o caractere '@'.")

        self.__email = email

    @property
    def senha_hash(self):
        """
        Getter para senha_hash
        :return: str - Hash da senha do usuário
        """
        return self.__senha_hash

    @senha_hash.setter
    def senha_hash(self, value):
        """
        Define o hash da senha do usuário.

        🔹 Regra de domínio: garante que o hash seja sempre uma string não vazia.

        :param value: str - Hash da senha do usuário.
        :raises ValueError: Lança erro se o valor não for string, estiver vazio ou for None.

        Exemplo:
        >>> usuario = Usuario()
        >>> usuario.senha_hash = "hash_da_senha"   # ✅ válido
        >>> usuario.senha_hash = ""                # ❌ lança erro
        >>> usuario.senha_hash = None              # ❌ lança erro
        """
        if value is None:
            raise ValueError("senha_hash não pode ser None.")

        if not isinstance(value, str):
            raise ValueError("senha_hash deve ser uma string.")

        senha_hash = value.strip()
        if len(senha_hash) == 0:
            raise ValueError("senha_hash não pode estar vazio.")

        self.__senha_hash = senha_hash

    @property
    def empresa(self):
        """
        Getter para empresa
        :return: str - Nome da empresa do usuário
        """
        return self.__empresa

    @empresa.setter
    def empresa(self, value):
        """
        Define a empresa do usuário.

        :param value: str - Nome da empresa (pode ser None)
        """
        if value is None:
            self.__empresa = None
            return

        if not isinstance(value, str):
            raise ValueError("empresa deve ser uma string.")

        self.__empresa = value.strip()

    @property
    def perfil_tipo(self):
        """
        Determina automaticamente o tipo de perfil baseado no campo empresa
        """
        if not self.__empresa or self.__empresa.strip() == "":
            return "pessoal"
        else:
            return "profissional"
        
    @perfil_tipo.setter
    def perfil_tipo(self, value):
        """
        Getter para perfil_tipo
        """
        if value is None:
            self.__perfil_tipo = None
            return
        
        if not isinstance(value, str):
            raise ValueError("perfil_tipo deve ser uma string!")
        
        self.__perfil_tipo = value.strip()

    @property
    def hierarquia(self):
        """
        Determina automaticamente a hierarquia
        """
        return self.__hierarquia
    
    @hierarquia.setter
    def hierarquia(self, value):
        """
        Getter para perfil_tipo
        """
        if value is None:
            self.__hierarquia = None
            return
        
        if not isinstance(value, str):
            raise ValueError("hierarquia deve ser uma string!")
        
        self.__hierarquia = value.strip()

    @property
    def data_atualizacao(self):
        """
        Getter para data_atualizacao
        :return: datetime - Data de criação do usuário
        """
        return self.__data_atualizacao

    @data_atualizacao.setter
    def data_atualizacao(self, value):
        """
        Define a data de criação do usuário.

        🔹 Regra de domínio: garante que a data seja um objeto datetime.

        :param value: datetime - Data de criação do usuário.
        :raises ValueError: Lança erro se o valor não for datetime.

        Exemplo:
        >>> usuario = Usuario()
        >>> from datetime import datetime
        >>> usuario.data_atualizacao = datetime.now()   # ✅ válido
        >>> usuario.data_atualizacao = "2023-01-01"     # ❌ lança erro
        """
        if value is None:
            self.__data_atualizacao = None
            return
            
        from datetime import datetime
        if not isinstance(value, datetime):
            raise ValueError("data_atualizacao deve ser um objeto datetime.")

        self.__data_atualizacao = value

    @property
    def data_atualizacao(self):
        """
        Getter para data_atualizacao
        :return: datetime - Data de atualização do usuário
        """
        return self.__data_atualizacao
        
    @data_atualizacao.setter
    def data_atualizacao(self, value):
        """
        Define a data de atualização do usuário.

        :param value: datetime - Data de atualização do usuário.
        """
        if value is None:
            self.__data_atualizacao = None
            return
            
        from datetime import datetime
        if not isinstance(value, datetime):
            raise ValueError("data_atualizacao deve ser um objeto datetime.")

        self.__data_atualizacao = value

    def to_dict(self):
        """
        Converte o objeto Usuario para dicionário
        """
        return {
            'id': self.__id,
            'nome': self.__nome,
            'email': self.__email,
            'empresa': self.__empresa,
            'perfil_tipo': self.__perfil_tipo,
            'hierarquia': self.__hierarquia,
            'data_atualizacao': self.__data_atualizacao.strftime('%Y-%m-%d %H:%M:%S') if self.__data_atualizacao else None,
            'data_atualizacao': self.__data_atualizacao.strftime('%Y-%m-%d %H:%M:%S') if self.__data_atualizacao else None
        }
    