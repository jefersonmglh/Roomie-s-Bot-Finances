import telebot
from var_config import BOT_TOKEN
from function_calls import *
import time
import os
import traceback


bot = telebot.TeleBot(BOT_TOKEN)

calls = Calls(bot)

# HANDLERS

@bot.message_handler(commands=['start', 'help', 'ajuda'])
def help_call(message):
    calls.all_msgs(message)

@bot.message_handler(commands=['add'])
def add_call(message):
    calls.add(message)

@bot.message_handler(commands=['add_fixas'])
def add_call(message):
    calls.add_fixas(message)


@bot.message_handler(commands=['relatorios'])
def relatorios_call(message):
    try:
        calls.relatorios(message)
    except Exception as e:
        print(e)
        print(traceback.format_exc())

@bot.message_handler(commands=['relatorio_basico_mensal'])
def relatorio_basico_call(message):
    try:
        calls.relatorio_basico(message)
    except Exception as e:
        print(e)        
        print(traceback.format_exc())
        print('basico')
        

@bot.message_handler(commands=['relatorio_mensal_e_fechar_mes'])
def fechar_mes_relatorio(message):
    try:
        calls.completo_mensal(message)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        print('completo_mensal')
    

@bot.message_handler(commands=['fixas'])
def fixas_info_call(message):
    calls.fixas_info(message)


@bot.message_handler(commands=['modificar_fixas'])
def modificar(message):
    try:
        calls.mod_fixas(message)
    except Exception as e:
        print(e)        
        print(traceback.format_exc())


@bot.message_handler(func=lambda message: True)
def all_msgs_call(message):
    calls.all_msgs(message)

@bot.callback_query_handler(func=lambda call: call.data == 'conf_no')
def all_msgs_call2(message):
    calls.all_msgs(message)


if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling()
