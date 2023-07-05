from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from db_manager import *
import objects
from frase import CNQuotes
from io import BytesIO





class Calls:
    def __init__(self, bot):
        self.bot = bot
        self.db = DataBaseManager()
# inline fuctions
    def gen_markup(self):
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton("Sim", callback_data="conf_yes"),
                   InlineKeyboardButton("Não", callback_data="conf_no"))
        return markup

    def gen_markup2(self):
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton("Sim", callback_data="conf_yes2"),
                   InlineKeyboardButton("Não", callback_data="conf_no"))
        return markup

    def gen_markup3(self):
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton("Sim", callback_data="conf_yes3"),
                   InlineKeyboardButton("Não", callback_data="conf_no"))
        return markup
    def gen_markup4(self):
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton("Sim", callback_data="conf_yes4"),
                   InlineKeyboardButton("Não", callback_data="conf_no"))
        return markup

    # functions calls
    def help_str(self, message):
        self.bot.reply_to(message, '''
      Para adicionar um valor, mande a mensagem no seguinte formato:
      /add 'descrição' 'valor' --------- Exemplo: "/add ifood 89.50"
      .
      /fixas para modificar o valor de algum gasto fixo
      .
      /add_fixas adiciona um gasto fixo nas contas
      .
      /relatorios dos gastos
      .
      /mamada para ganhar uma.   
      .
      ''')


    def add(self, message):
        raw_msg = message.text.split(' ')
        if len(raw_msg) < 3:
            self.bot.reply_to(message, '''
                     Por favor, para adicionar um valor, coloque o comando '/add' + descrição do gasto + valor do gasto.
                     Exemplo: "/add ifood 100"
                     ''')
        else:
            global msg
            msg = objects.Format_Message(message)
            confirmation = f"{msg.user}, você confirma a adição do gasto {msg.desc}, no valor de {msg.value}? Aperte Sim para confirmar."
            self.bot.reply_to(message, confirmation, reply_markup=self.gen_markup())

            @self.bot.callback_query_handler(func=lambda call: call.data == 'conf_yes')
            def callback_query(call):
                print('callback1')
                self.bot.reply_to(message, msg.add_db())

    def add_fixas(self, message):
        raw_msg = message.text.split(' ')
        if len(raw_msg) < 3:
            self.bot.reply_to(message, '''
                     Por favor, para adicionar um valor, coloque o comando '/add_fixas' + descrição do gasto fixo + valor do gasto.
                     Exemplo: "/add ifood 100"
                     ''')
        else:
            global msg
            msg = objects.Format_Message(message)
            confirmation = f"{msg.user}, você confirma a adição do gasto fixo {msg.desc}, no valor de {msg.value}? Aperte Sim para confirmar."
            self.bot.reply_to(message, confirmation, reply_markup=self.gen_markup4())

            @self.bot.callback_query_handler(func=lambda call: call.data == 'conf_yes4')
            def callback_query(call):
                print('callback4')
                self.bot.reply_to(message, msg.add_fixas_db())


    def relatorios(self, message):
        global data_relatorios        
        data_relatorios = objects.Relatorios(message)
        table = '''
      /relatorio_basico_mensal  
/relatorio_mensal_e_fechar_mes
        '''

        self.bot.reply_to(message, table)


    def relatorio_basico(self, message):
        
        df_basico_mensal = data_relatorios.df_ultimo_no_fixas()
        try:
            df_str = df_basico_mensal.to_string(columns=['user', 'value', 'desc'],
                                                index=False, header=True,
                                                line_width=100, justify='center')
        except:
            self.bot.reply_to(message, 'sem lançamentos')
        else:
            gastos_total = df_basico_mensal['value'].sum()
            grouped_user = df_basico_mensal.groupby('user').sum()
            self.bot.reply_to(message, f'''
            Até o momento foi gasto o total de ${round(gastos_total, 2)}. ''')
            self.bot.reply_to(message, df_str)
            for usuario in grouped_user.index:
                valor = grouped_user.loc[usuario, "value"]
                self.bot.reply_to(message, f'{usuario} gastou até o momento ${round(valor, 2)}.')
            
     


    def completo_mensal(self, message):
        
        df_basico_mensal = data_relatorios.df_ultimo_no_fixas()
        try:
            df_str = df_basico_mensal.to_string(columns=['user', 'value', 'desc'],
                                                index=False, header=True,
                                                line_width=100, justify='center')
        except:
            self.bot.reply_to(message, 'sem lançamentos')
        else:
            self.bot.reply_to(message, df_str)
            job = data_relatorios.relatorio_completo_mensal()
            print('init jobbing')
            for k, v in job.items():
                if k == 'diff_dic':
                    for user, value_ in v.items():
                        if value_ > 0:
                            self.bot.reply_to(message, f'O {user} precisa receber: ${value_}')
                        else:
                            self.bot.reply_to(message, f'O {user} precisa pagar: ${value_ * (-1)}')

                else:
                    self.bot.send_photo(chat_id=message.chat.id, photo=v)

            self.bot.reply_to(message,'Deseja fazer o fechamento do mês?', reply_markup=self.gen_markup2())
            @self.bot.callback_query_handler(func=lambda call: call.data == 'conf_yes2')
            def callback_query2(call):
                print('callback2')           
                conf_ = data_relatorios.fechar_mes()
                self.bot.reply_to(message, f'Fechamento concluído com sucesso.\n id: {conf_}')


    def fixas_info(self, message):
        for doc in self.db.all_fixas():
            self.bot.reply_to(message, f'''    
    
            Descrição: {doc['desc']}, 
            Usuário padrão de pagamento: {doc['user']},
            Valor de {doc['value']}.''')

        self.bot.reply_to(message, f'''
        Para alterar o valor do gasto, coloque o comando /modificar_fixas+descrição+valor
      Exemplo: "/modificar_fixas aluguel 2600"
        ''')


    def mod_fixas(self, message):
        raw_msg = message.text.split(' ')
        if len(raw_msg) < 3:
            self.bot.reply_to(message, '''
                     Por favor, para modificar um gasto fixo, coloque o comando '/modificar' + descrição do gasto fixo + valor do gasto.
                     Exemplo: "/modificar_fixas aluguel 100"
                     ''')
        else: 
            mod_f = objects.Format_Message(message)
            doc_finded = {}

            for doc in self.db.all_fixas():
                if mod_f.desc == doc['desc']:
                    doc_finded = doc
                    break
                
            if doc_finded:
                conf = f"Você confirma a modificação do gasto {doc_finded['desc']} no valor de {doc_finded['value']} para o novo valor de {mod_f.value}?"
                self.bot.reply_to(message, conf, reply_markup=self.gen_markup3())
            else:
                self.bot.reply_to(message, 'Gasto fixo não encontrado pela palavra chave. Para adicionar um gasto fixo utilize o comando /add_fixas')

            @self.bot.callback_query_handler(func=lambda call: call.data == 'conf_yes3')
            def callback_query(call):
                print('callback3')
                try:
                    print(doc_finded)
                    self.bot.reply_to(message, mod_f.mod_fixas_db(doc_finded['_id']))
                except Exception as e:
                    print(e)
                    print(traceback.format_exc())


    def all_msgs(self, message):
        time = objects.ConverterTimeStamp(message.date)
        self.bot.reply_to(message, f'''
    {time.period}, {message.from_user.first_name}.
    Aqui vai uma frase do ChuCk Norris p vc:
    
    
    
    "{CNQuotes().quote}"\n\n
    
    Comandos:
    /add
    /add_fixas
    /fixas
    /relatorios
    
    
    Para ajuda, digite /help
    ''')
