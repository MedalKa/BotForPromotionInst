
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import logging
from functools import wraps

import apiai, json
import requests
import re
import datetime


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


# Обработка команд
def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Привет, я бот, который многое знает о продвижение в Instagram.\U0001F393 Я могу помочь Вам с этим.\nЧтобы узнать чем я могу Вам помочь, наберите \"/help\"')

#@updater.message_handler(commands=['start', 'description'])
def start(bot, update):
    bot.send_message(chat_id=update.message.chat.id,
                          text="Привет, я бот, который многое знает о продвижение в Instagram.\U0001F393 Я могу помочь Вам с этим.\nЧтобы узнать чем я могу Вам помочь, наберите \"/help\"")

#@updater.message_handler(commands=['help'])
def help(bot, update):
    bot.send_message(chat_id=update.message.chat.id,
                          text="Я умею:\n/description-показать описание\n/ways-вывести способы продвижения\n/hashtag-помочь с подбором хештегов\n")


def ways_promotion(bot, update):
	 bot.send_message(chat_id=update.message.chat.id,
                          text="Выберите один из способов продвижения, чтобы узнать подробнее.", reply_markup=draw_button_for_ways())

def draw_button_for_ways():
    keys =[[InlineKeyboardButton('Продвижение контентом', callback_data='1')],
	[InlineKeyboardButton('Таргетированная реклама', callback_data='2')],
	[InlineKeyboardButton('Рекламные объявления на страницах сообществ', callback_data='3')],
	[InlineKeyboardButton('Конкурсы и акции', callback_data='4')],
	[InlineKeyboardButton('Обмен рекламой', callback_data='5')],
	[InlineKeyboardButton('Публикация хештегов', callback_data='6')]]
    return InlineKeyboardMarkup(inline_keyboard=keys)

def get_callback_from_button_for_ways(bot, update):
	query = update.callback_query
	username = update.effective_user.username
	chat_id = query.message.chat.id
	message_id = query.message.message_id
	if int(query.data) == 1:
		bot.send_message(chat_id=chat_id, message_id=message_id, 
		text="В социальные сети люди заходят для того, чтобы пообщаться и отдохнуть. Поэтому интересный контент пользуется популярностью. Создание привлекательных постов, которые понравятся пользователям, является популярным инструментом для продвижения в Инстаграм.", reply_markup=draw_button_for_ways())
	if int(query.data) == 2:
		bot.send_message(chat_id=chat_id, message_id=message_id, 
		text="Таргетированная реклама представляет собой объявления небольшого размера, которые могут находиться в разных областях страницы в социальной сети. Обычно они включают себя изображение и соответствующую подпись к нему. Такая реклама видна не всем пользователям. Она отображается лишь для целевой аудитории. Вы можете настроить такую рекламу исходя из требований к потенциальным клиентам. Можно выбрать один из двух вариантов оплаты за подобную рекламу: за количество кликов по ней и число показов.")
		bot.send_photo(chat_id=chat_id, photo='http://instaking.ru/wp-content/uploads/2013/03/1.jpg',reply_markup=draw_button_for_ways())
	if int(query.data) == 3:
		bot.send_message(chat_id=chat_id, message_id=message_id, 
		text="Можно рекламировать свои товары и услуги на страницах тематических сообществ. В зависимости от характеристик сообщества (тематика, количество подписчиков и их активность и т.д.) цена такой рекламы может существенно отличаться. При публикации подобной рекламы важно не только указать коммерческую информацию, но и опубликовать призыв к действию. Для этого можно организовать акции или розыгрыши.", reply_markup=draw_button_for_ways())					  
	if int(query.data) == 4:
		bot.send_message(chat_id=chat_id, message_id=message_id, 
		text="Это очень эффективный инструмент продвижения коммерческих аккаунтов. Например, часто запускаются конкурсы, по условиям которых победитель будет определяться случайным образом среди пользователей, поделившихся с подписчиками конкретной записью. В результате посетители страницы начинают делиться информацией со своими друзьями, обеспечивая рекламу продвигаемого бренда. Эффективность данного метода продвижения заключается в том, что многие хотят получить возможность бесплатно выиграть подарок, не затратив при этом много сил и времени.", reply_markup=draw_button_for_ways())
	if int(query.data) == 5:
		bot.send_message(chat_id=chat_id, message_id=message_id, 
		text="Можно договориться о взаимной рекламе с компанией, которая работает в похожей нише, и имеет ту же самую целевую аудиторию. Также можно организовать совместную деятельность по привлечению клиентов путем организации тематических марафонов и других проектов.", reply_markup=draw_button_for_ways())
	if int(query.data) == 6:
		bot.send_message(chat_id=chat_id, message_id=message_id, text="Каждый пост желательно оформлять с помощью хэштегов, которые непосредственно связаны с темой публикации. Хештеги для Инстаграма используются для маркировки фото и их поиска. Важно использовать актуальные хештеги, через которые пользователи соцсети смогут найти ваш контент. Мы уже собрали в нашем боте все необходимые хештеги, для этого использутей /hashtag. Вам остаётся скопировать и добавить к своему посту. Это поможет привлечь новых потенциальных клиентов.", reply_markup=draw_button_for_ways())
		
		
def send_hashtags(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Хештеги для Инстаграма используются для маркировки фото и их поиска. Важно использовать актуальные хештеги, через которые пользователи соцсети смогут найти ваш контент. Мы уже собрали все необходимые хештеги. Вам остаётся скопировать и добавить к своему посту.\nВыберите категорию хештегов, пожалуйста:", reply_markup=draw_button_with_hashtags())

def draw_button_with_hashtags():
    keys =[[InlineKeyboardButton('Популярные на русском', callback_data='7'),InlineKeyboardButton('Популярные на английском', callback_data='8')],
	[InlineKeyboardButton('Для лайков', callback_data='9'),InlineKeyboardButton('Для подписок', callback_data='10')],
	[InlineKeyboardButton('Спорт', callback_data='11'),InlineKeyboardButton('Еда', callback_data='12')],
	[InlineKeyboardButton('Животные', callback_data='13'),InlineKeyboardButton('Природа', callback_data='14')]]
    return InlineKeyboardMarkup(inline_keyboard=keys)

def get_callback_from_button_with_hashtags(bot, update):
	query = update.callback_query
	username = update.effective_user.username
	chat_id = query.message.chat.id
	message_id = query.message.message_id
	if int(query.data) == 7:
		bot.send_message(chat_id=chat_id, message_id=message_id, 
		text="#инстаграм #инстаграманет #инстаграмнедели #инстаграм_порусски #инста #инстатаг #я #улыбка #селфи #красота #супер #день #ночь #природа #друзья #дружба #лайки #фото #фотография #россия #украина #любовь #любовьмоя #девушки #москва #жизнь #жизньпрекрасна #небо")
	if int(query.data) == 8:
		bot.send_message(chat_id=chat_id, message_id=message_id, 
		text="#love #instagood #me #tbt #cute #follow #followme #photooftheday #happy #beautiful #selfie #picoftheday #like4like #instagramanet #instatag #smile #friends #fun #fashion #summer #instadaily #igers #instalike #swag #amazing #tflers #follow4follow #likeforlike #bestoftheday #l4l")
	if int(query.data) == 9:
		bot.send_message(chat_id=chat_id, message_id=message_id, 
		text="#likes #likesforlikes #likes4likes #likesforfollow #likebackteam #likesreturned #likesforlike #l4l #liker #liketeam #likeback #like4like #like4follow #like4likes #instagramanet #лайки #лайкивзаимно #лайкничокакнеродная #нравится #лайкнименя #лайкни #лайкизалайки #лайкиинстаграм #лайкивинстаграм #лайкивинстаграме #лайквзаимно #инстаграманет #инстаграм_порусски")
	if int(query.data) == 10:
		bot.send_message(chat_id=chat_id, message_id=message_id, 
		text="#follow #followme #follow4follow #followforfollow #followback #followher #followhim #followall #follows #f4f #instatag #teamfollowback #pleasefollow #pleasefollowme #followbackteam #following #followers #instagramanet #следуй #следуйзамной #подпишись #подпишисьнаменя #подпишисьвзаимно #подписка #инстаграм #инстаграманет #инстатаг #девушка #девушки #взаимнаяподписка") 
	if int(query.data) == 11:
		bot.send_message(chat_id=chat_id, message_id=message_id, 
		text="#sport #sports #sporty #sportsday #instasport #instasports #instagramanet #instatag #win #winning #gametime #спорт #спортзал #спортсмен #спортэтожизнь #спортсмены #спортсила #спортивноетело #спортивнаясемья #спортлайф #спортклуб #спортрежим #инстаспорт #инстаграманет #инстатаг #здоровье #здоровоепитание #здоровыйобразжизни")
	if int(query.data) == 12:
		bot.send_message(chat_id=chat_id, message_id=message_id, 
		text="#instafood #instagramanet #instatag #food #foodporn #foodie #foodgasm #foodpics #foodpic #foodstagram #foods #foodphotography #еда #едаялюблютебя #едаеда #едадляжизни #едатопливо #инстаеда #инстаграманет #инстатаг #блюдо #блюда  #вкусно #вкусняшка #вкусняшки #вкуснятина #вкусности #вкусноиполезно #вкуснота")
	if int(query.data) == 13:
		bot.send_message(chat_id=chat_id, message_id=message_id, 
		text="#animal #animals #animallovers #animales #instagramanet #instatag #pet #pets #petstagram #petsagram #petsofinstagram #pets_of_instagram #petscorner #petoftheday #животные #животныймир #вмиреживотных #мимими #мимимишность #мимишность #лапочка #мордочка #инстаграманет #инстатаг #питомец #питомцы #фауна #мирживотных #природа")
	if int(query.data) == 14:
		bot.send_message(chat_id=chat_id, message_id=message_id, 
		text="#nature #naturelovers #nature_perfection #natureza #naturelover #naturehippys #instagramanet #instatag  #nature_shooters #natureporn #natureaddict #pretty #nice #photooftheday #weather #природа #воздух #природароссии #люблюприроду #инстатаг #живаяприрода #инстаграманет #природапрекрасна #наприроде #наприроду #наприродехорошо #люблюнебо #открытиесезона #природароссии #природапрекрасна")	
	
def error(bot, update):
    logger.warning('Update "%s" caused error "%s"', bot, update.error)
	
def main():
	updater = Updater(token='1155698876:AAESYB6A8-mK7fGtf4aWFP3amJ9SZKqcaMY')
	dispatcher = updater.dispatcher
	
	start_command_handler = CommandHandler('start', startCommand)
	description_comand_handler = CommandHandler('description', start)
	help_comand_handler = CommandHandler('help', help)
	ways_comand_handler = CommandHandler('ways', ways_promotion)
	hashtag_comand_handler = CommandHandler('hashtag', send_hashtags)
	hashtags_callback_query_handler = CallbackQueryHandler(get_callback_from_button_with_hashtags)
	ways_callback_query_handler = CallbackQueryHandler(get_callback_from_button_for_ways)
	
	dispatcher.add_handler(start_command_handler)
	dispatcher.add_handler(start_command_handler)
	dispatcher.add_handler(description_comand_handler)
	dispatcher.add_handler(help_comand_handler)
	dispatcher.add_handler(ways_comand_handler)
	dispatcher.add_handler(hashtag_comand_handler)
	dispatcher.add_error_handler(error)
	dispatcher.add_handler(ways_callback_query_handler)
	dispatcher.add_handler(hashtags_callback_query_handler)

	updater.start_polling(clean=True)

	updater.idle()
	
if __name__ == '__main__':
	main()
