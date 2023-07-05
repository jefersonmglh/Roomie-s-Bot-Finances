from datetime import timedelta, datetime
import pandas as pd
import matplotlib.pyplot as plt
from db_manager import *
from io import BytesIO
import numpy as np

db = DataBaseManager()

class ConverterTimeStamp:

  def __init__(self, timestamp):
    self.timestamp = timestamp
    self.timeutc_gmt = datetime.utcfromtimestamp(self.timestamp) - timedelta(hours=3)
    if self.timeutc_gmt.strftime('%H:%M') > '00:00' and self.timeutc_gmt.strftime('%H:%M') < '12:00':
      self.period = "Bom dia"
    elif self.timeutc_gmt.strftime('%H:%M') > '12:00' and self.timeutc_gmt.strftime('%H:%M') < '18:00':
      self.period = "Boa tarde"
    else:
      self.period = "Boa noite"



class Format_Message:

  def __init__(self, message):
    self.raw_msg = message.text.split(' ')
    self.user = message.from_user.first_name
    self.time = message.date
    self.desc = str(self.raw_msg[1])
    self.value = float(self.raw_msg[2])
    self.biblio = {}
    self.biblio['user'] = self.user
    self.biblio['value'] = self.value
    self.biblio['desc'] = self.desc
    self.biblio['time'] = self.time
  
  def add_db(self):
    conf = db.add_currently(self.biblio)
    return f'Adicionado com sucesso.\nid : {conf}'

  def add_fixas_db(self):
    conf_ = db.add_fixas(self.biblio)
    return f'Adicionado com sucesso.\nid : {conf_}'
  
  def mod_fixas_db(self, doc_id):
    try:
      conf_ = db.mod_fix(doc_id=doc_id, value_data=self.value, user_data=self.user)
      print(f'mod_conf_ = {conf_}')
    except Exception as e:
      print(e)
      print(traceback.format_exc())
      return None
    else:   
      print(conf_)
      return f'Modificado com sucesso.\nid : {conf_}'



class Relatorios:

  def __init__(self, message):


    self.fechamento_datas = [doc['time'] for doc in db.fechamento_data()]
    self.atual_data = message.date
    self.user = message.from_user.first_name
    self.user_list = self.search_users()


  def df_ultimo(self):
    self.df_gastos = pd.DataFrame(list(db.docs_per_data(self.fechamento_datas[0])))
    self.df_fixas = pd.DataFrame(list(db.all_fixas()))
    self.df_fixas['time'] = None
    self.df = pd.concat([self.df_gastos, self.df_fixas], axis=0, ignore_index=True)
    return self.df

  def df_ultimo_no_fixas(self):
    return pd.DataFrame(list(db.docs_per_data(self.fechamento_datas[0])))

  def fechar_mes(self):
    id_fechamento = db.add_currently({"user": self.user, "desc": "fechamento", "time": self.atual_data})
    return id_fechamento

  def search_users(self):
    return list(self.df_ultimo()['user'].unique())

  def diff_p_user(self):
    df = self.df_ultimo()
    media_p_usuario = df['value'].sum()/len(self.user_list)
    grouped_user = df.groupby('user').sum(numeric_only=True)
    dif_p_user = {}
    for usuario in grouped_user.index:
        valor = grouped_user.loc[usuario, "value"]
        dif_p_user[usuario] = valor - media_p_usuario

    return dif_p_user



  def relatorio_completo_mensal(self):

    df = self.df_ultimo()
    df_nofix = self.df_ultimo_no_fixas()

    if len(df) > 1:
      grouped_desc = df.groupby('desc').sum(numeric_only=True)
      grouped_desc = grouped_desc.sort_values('value', ascending=False)
      fig, axs = plt.subplots(1, 2, figsize=(10, 5))
      fig.autofmt_xdate(rotation=45)

      # Gráfico 1 - DESC
      colors1 = plt.cm.rainbow(np.linspace(0, 1, len(grouped_desc.index)))
      axs[0].bar(grouped_desc.index, grouped_desc['value'], color=colors1)

      for i, v in enumerate(grouped_desc['value']):
        axs[0].text(i, v, str(round(v, 2)), ha='center')


      axs[0].set_ylabel('Valor')
      fech_1 = ConverterTimeStamp(self.fechamento_datas[0])
      axs[0].set_title('Com gastos fixos')


      grouped_desc_nofix = df_nofix.groupby('desc').sum(numeric_only=True)
      grouped_desc_nofix = grouped_desc_nofix.sort_values('value', ascending=False)

      colors2 = plt.cm.rainbow(np.linspace(0, 1, len(grouped_desc_nofix.index)))
      axs[1].bar(grouped_desc_nofix.index, grouped_desc_nofix['value'], color=colors2)

      for i, v in enumerate(grouped_desc_nofix['value']):
        axs[1].text(i, v, str(round(v, 2)), ha='center')


      axs[1].set_ylabel('Valor')
      axs[1].set_title('Sem gastos fixos')

      
      fig.suptitle("Gastos por descrição\nPeríodo: {} a {}".format(fech_1.timeutc_gmt.strftime('%d-%m'), datetime.now().strftime('%d-%m')))
      bar1 = BytesIO()
      fig.savefig(bar1, format='png')
      bar1.seek(0)

      #Grafico 2 - USER

      fig1, axs1 = plt.subplots(1, 2, figsize=(10, 5))
      fig1.autofmt_xdate(rotation=45)

      #W/ FIXAS
      grouped_user = df.groupby('user').sum(numeric_only=True)
      grouped_user = grouped_user.sort_values('value', ascending=False)

      colors3 = plt.cm.rainbow(np.linspace(0, 1, len(grouped_user.index)))
      axs1[0].bar(grouped_user.index, grouped_user['value'], color=colors3)

      for i, v in enumerate(grouped_user['value']):
        axs1[0].text(i, v, str(round(v, 2)), ha='center')


      axs1[0].set_ylabel('Valor')
      axs1[0].set_title('Com gastos fixos')


      grouped_user_nofix = df_nofix.groupby('user').sum(numeric_only=True)
      grouped_user_nofix = grouped_user_nofix.sort_values('value', ascending=False)

      colors4 = plt.cm.rainbow(np.linspace(0, 1, len(grouped_user_nofix.index)))
      axs1[1].bar(grouped_user_nofix.index, grouped_user_nofix['value'], color=colors4)

      for i, v in enumerate(grouped_user_nofix['value']):
        axs1[1].text(i, v, str(round(v, 2)), ha='center')

      axs1[1].set_ylabel('Valor')
      fech_2 = ConverterTimeStamp(self.fechamento_datas[0])
      axs1[1].set_title('Sem gastos fixos')


      fig1.suptitle("Gastos por usuário\nPeríodo: {} a {}".format(fech_1.timeutc_gmt.strftime('%d-%m'), datetime.now().strftime('%d-%m')))
      bar2 = BytesIO()
      fig1.savefig(bar2, format='png')
      bar2.seek(0)

      return {
            'img_user': bar1,
            'img_desc': bar2,
            'diff_dic': self.diff_p_user()
      }

      
