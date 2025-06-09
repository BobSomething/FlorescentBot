from typing import Final, Dict
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes
import logging

from datetime import datetime as d

import pytz

TOKEN: Final = 'TOKEN'

BOT_USERNAME: Final = 'BotUsername'

# Logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

events : list = [d(year = 2024, month = 4, day = 22, hour = 21), #Revelation Night
                 d(year = 2024, month = 4, day = 23, hour = 17), #Fun Fair
                 d(year = 2024, month = 4, day = 24, hour = 10, minute = 30), #Sport Festival
                 d(year = 2024, month = 4, day = 25, hour = 11, minute = 30), #Food Fiesta
                 d(year = 2024, month = 4, day = 26, hour = 0), #Glow Party
                 d(year = 2024, month = 4, day = 26, hour = 19), #TriPromo Dinner
                 d(year = 2024, month = 4, day = 27, hour = 18), #Pub Quiz
                 d(year = 2024, month = 4, day = 25, hour = 10) #Flower Pot Painting Brunch
                 ]

events_details = ['Revelation Night', 'Fun Fair /fun_fair_activities', 'Sport Festival', 
                  'Food Fiesta /menu_fiesta', 'Glow Party',
                  'TriPromo Dinner', 'Pub Quiz', 'Flower Pot Painting Brunch']

menu_general = ['Plain Crêpe', 'Jam Crêpe', 'Nuttela Crêpe', 'Scrambled Crêpe', 'DIY Crêpe, we bring batter']

food_drink = 12

menu_fiesta = ['Chile con carne', 'Curry', 'Pasta', 'Hot Dogs', 'Stir Fried Veggies']

fun_fair_act = ['Basketball Shootout', '3 legged race', 'Beer pong', 'Limbo', 'Eating Contest', 'Tug of War',
                'Mummy', 'Ankle Balloon']

# Commands

async def social_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Our website: [Florescent](http://florescent.fr)\n', parse_mode='MarkdownV2')
    await update.message.reply_text('Our instagram: @florescent.bx')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('*capybara sounds*', parse_mode='MarkdownV2')
    await update.message.reply_text('Hi! I’m Flora, the 11th member of Fl’Orescent🌼. '
                                    'This week, I’m here to assist you with all your desires. '
                                    'Whether it be crepes, event schedules or simply a chat if you’re lonely ;) '
                                    'Look out for my bright pink bikini 🫦')
    await update.message.reply_text('So you’ve chosen to embark on this adventure with us, ' 
                                    'let me _illuminate_ the path for you！\n' 
                                    'You can choose any of our _twinkling_ trails:', parse_mode='MarkdownV2')
    await update.message.reply_text('/members - to discover our members,\n'
                                    '/food - to order out goodies,\n'
                                    '/help - for all the commands')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Helping incoming. Here is the full list of commands:\n'
                                    '・/start - Starting Flora\n'
                                    '・/members - About our members\n'
                                    '・/menu - Look at our menu\n'
                                    '・/food - Order some food, stop your hunger!\n'
                                    '・/events - Discover our events\n'
                                    '・/next_event - Countdown for our next event!\n'
                                    '・/social - Go check our social medias!\n'
                                    '・/help - List all commands\n')
    
async def members_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Fl’Orescent’s radiant team consists of:\n'
                                    '・*General Secretary:* _Julia Benhamou_\n'
                                    '・*Professional Relations:* _Emeric Payer_\n'
                                    '・*Internal Relations:* _Horace Blachez_\n'
                                    '・*Treasurer:* _Carla Guinea Carranza_\n'
                                    '・*Communication:* _Vashti Chowla_\n'
                                    '・*Committees & Binets:* _Sacha Gregoire_\n'
                                    '・*Integration:* _Mael Kupperschmitt_\n'
                                    '・*Events:* _Alexander Moller Rivera_\n'
                                    '・*Sports:* _Matteo Sainton_\n'
                                    '・*Infrastructure:* _Reda Boyer_\n',
                                    parse_mode='MarkdownV2')

quests = ['・Most standard kitchen chairs in a single kitchen:\n \t\t',
          '・Most crepes eaten in one minute (filling required) 🥞:\n \t\t',
          '・Longest handshake with Barthelemy (he is warned) 🤝:\n \t\t',
          '・Maximum amount of people in your own bathroom (only non-disabled bathrooms) 🚽:\n \t\t',
          "・Maximum amount of water dumped on Horace's head (blonde buzzed cut guy) (outdoors):\n \t\t",
          "・Fastest to chug an entire Obe:\n \t\t",
          "・Furthest Kitchen Chair from Campus (Calculated from the address 103 avenue Henri Becquerel):\n \t\t",
          '・Most extreme make up look 💄:\n \t\t',
          '・Most Push Ups in 1 minute (chest to ground) 💪: \n \t\t',
          '・Most Glowing and Florescent Outfit 😫💜: \n \t\t',
          '・Most whole Chicken Eggs in one hand 🥚 🖐️:\n \t\t'
          ]

record = ['@filipinorupchini, @paul_mtht, @nic0las_h and @Ryan_Sfeila with 88 chairs!!',
          'Krzysztof Kujawa with 6 crêpes!!',
          'Abhigyan Prakash with 7 minutes and 15 seconds',
          "27 people in a bathroom with the lead of Antonia Gerlach and Losel Matos!",
          'Krzysztof Kujawa with 10L of water 💦',
          "Léopold Rousseau with 8 seconds!",
          "Adam Madrisotti with 99.9 km (Middle of Nowhere)",
          "Wojtek Ściuk with super extreme makeup!!",
          'Martin Delos with 69 Push Ups!',
          'Wojtek Ściuk with most Glowing and Florescent outfit 💛',
          'Wojtek Ściuk with 14 eggs!'
          ]
#58 push ups

async def records_rules_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌺 Fl’Orescent 🌺is going to revive our long lasting tradition, the RECORD BOOK . "
                                   "📖 🏆Each night at MIDNIGHT we will post the daily quests for you to complete. "
                                   "To validate this record, send your video to @FlorescentRecords and we will manually review your footage. "
                                   "There will be small prizes every following night for that day's events, "
                                   "and the winner with the most records will receive a 🎁RICE COOKER 🎁at the pub quiz on saturday! "
                                   "To see quests and title holders, “/records” on the @FlorescentBot. "
                                   "Also use “/record_book” on the @FlorescentBot to see the current record holders!\n"
                                   "Records can be beaten at any point in time, but daily prizes are awarded to the winners of the day." 
                                    "\n\n\nStay tuned for epic challenges, and memorable nights. 💜")
    

async def records_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #print(f'Records: {update} -- {context.error}')
    nl = '\n'
    text : str = 'Today’s Fl’Orescent quests are the following:\n'
    
    for i in range(4):
        text += f'{quests[i]} {record[i]} {nl}{nl}'
    
    text += 'Send a video of your record to @FlorescentRecords and you might end up engraved in the record book!!'
    
    await update.message.reply_text(text)

    await update.message.reply_text('⚠️ WARNING ⚠️․ You win the battle, not the war ⚔️ ․ \n\n'
                                    'Daily prizes are awarded to the winner of the Quest by the end of 24 hours 🏅․\n\n' 
                                    'The winner of the *__RICE COOKER__* is awarded to whoever holds the most unique records before the PUB QUIZ ❪Saturday 18:00❫․ '
                                    'records before the PUB QUIZ ❪Saturday 18:00❫․ \n\n'
                                    'In other words, you CAN beat the records of previous days to try and win the final prize 🏆․',
                                    parse_mode='MarkdownV2')
    await update.message.reply_text('To find out all the records you can beat click on /record_book.\n\n'
                                    'For more information on the rules check out /records_rules')

async def record_book_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #print(f'Record Book: {update} -- {context.error}')
    nl = '\n'
    text : str = 'The Fl’Orescent Record Book:\n'
    
    for i in range(len(quests)):
        text += f'{quests[i]} {record[i]} {nl}{nl}'
        
    await update.message.reply_text(text)
    

async def next_event_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    timeParis = pytz.timezone("Europe/Paris") 
    NOW = d.now(timeParis)
    
    NOW = d(year=NOW.year, month=NOW.month, day=NOW.day, hour=NOW.hour, minute=NOW.minute, second=NOW.second)
    
    #Calculating next event!
    next_event = events[0]
    index : int = 0
    delta = next_event - NOW
    
    while int(delta.days) < 0 and index < len(events):
        index+=1
        next_event = events[index]
        delta = next_event - NOW
    
    #Check if there is no more events left
    if delta.days < 0:
        await update.message.reply_text('No more events :(')
        return
    
    days : int = int(delta.days)
    total_sec : int = int(delta.seconds)
    sec : int = total_sec % 60
    min : int = (total_sec // 60) % 60
    hours : int = (total_sec // 3600) % 24
    
    text : str = f'The next event {events_details[index]} is in: '
    
    time = {days : 'day', hours : 'hour', min : 'minute'}
    
    for (k,v) in time.items():
        if k > 0:
            text += f'{k} {v}'
            if k > 1:
                text += 's'
            text += ', '
        
    if sec != 0:
        text += f'{sec} second'
        if sec > 1 or sec == 0:
            text += 's'
    else:
        text = text[:-2]
    text += '!'
    
    await update.message.reply_text(text)

def listing(L : list):
    text_add : str = ''
    for (i,event) in enumerate(L):
        text_add += f"{i+1}․ {event}"
        text_add += '\n'
    return text_add

async def list_events_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text : str = 'Our events are:\n'
    text += listing(events_details)
    
    await update.message.reply_text(text)
    
async def food_menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text : str = 'Our menu is:\n'
    text += listing(menu_general)
    
    await update.message.reply_text(text)
    
async def food_fiesta_menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text : str = 'Our menu for Food Fiesta include:\n'
    text += listing(menu_fiesta)
    
    await update.message.reply_text(text)
    
async def fun_fair_activities_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text : str = 'Activities during Fun Fair include:\n'
    text += listing(fun_fair_act)
    
    await update.message.reply_text(text)
    
async def cancel_order_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    user_data.clear()
    await update.message.reply_text('You have cleared your order! If you want to order again, click on /food')

NOT_CREPPING = False

async def close_bot_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global NOT_CREPPING
    if update.message.chat_id == -1002129983196:
        NOT_CREPPING ^= True
        await update.message.reply_text(f'Not Crepping is now {NOT_CREPPING}')

#Temporary


CHOOSING, TYPING_REPLY = range(2)

reply_keyboard = [
    ["Food", "Drink", "Location"],
    ["Amount", "Name", "Done"]
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f"{key}: {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])

async def food_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if NOT_CREPPING:
        await update.message.reply_text(
        "Unfortunately, we deactivated this command for now.\n" 
        "Look forward to deliver more food later ;).\n"
        "In the meantime check out current events!",
        reply_markup=markup,
        ) 
        return
    
    await update.message.reply_text(
        "Although I normally only eat algae, " 
        "Fl’Orescent has informed me that you all have a more refined palette, " 
        "so we have a great selection available at all times of the day and night 🫦\n\n"
        "・To pick your food/drink, please click on the button *Food*\n"
        "・Tell us about your location by clicking on *Location* to help us deliver your order\n"
        "・Optionally, tell us your name by clicking on *Name* and the *Amount* of food you want to order！",
        parse_mode='MarkdownV2',
        reply_markup=markup,
    )

    return CHOOSING


async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data["choice"] = text

    if text.lower() == "food":
        reply_food = [[c] for c in menu_general[:food_drink]]
        await update.message.reply_text(f"Please give me your {text.lower()}. "
                                        "Please pick from the given pool. \n Else the order could be invalid",
                                        reply_markup=ReplyKeyboardMarkup(
                                            reply_food, one_time_keyboard=True #, input_field_placeholder="Good Food"
                                        ),
                                    )
    if text.lower() == "drink":
        reply_food = [[menu_general[-1]]] #[[c] for c in menu_general[food_drink:]]
        await update.message.reply_text(f"Please give me your {text.lower()}. "
                                        "Please pick from the given pool.\nElse the order could be invalid.",
                                        reply_markup=ReplyKeyboardMarkup(
                                            reply_food, one_time_keyboard=True #, input_field_placeholder="Good Food"
                                        ),
                                    )
    
    if text.lower() == "location":
        await update.message.reply_text(f"Please give me your {text.lower()}. Your answer must be as specific as possible."
                                        "\nFor example: 103.60.08b, Foyer near the pool table. \n"
                                        "Unclear location could be not realized :(")
    if text.lower() == "name":
        await update.message.reply_text(f"Please give me your {text.lower()}!")
        
    if text.lower() == "amount":
        await update.message.reply_text(f"Please specify how much food do you want! E.g. 3 crêpes")
        
    return TYPING_REPLY

async def received_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store info provided by user and ask for the next category."""
    user_data = context.user_data
    text = update.message.text
    category = user_data["choice"]
    user_data[category] = text
    del user_data["choice"]

    await update.message.reply_text(
        "So here’s what I have from you so far - please make sure not to gloss over any details 💅:\n"
        f"{facts_to_str(user_data)}" "\nIf your order is done - let me know by replying " 
        "Done so our brilliant chefs and team can get it to you 🧑‍🍳\n\n"
        "To cancel your order, click on /cancel_order",
        reply_markup=markup,
    )

    return CHOOSING


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the gathered info and end the conversation."""
    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]
    
    if "Location" not in user_data:
        await update.message.reply_text(
            "Hey, I think you did not give us your current location, please let us know where to deliver"
            " by clicking on *Location* and typing your location！",
            parse_mode='MarkdownV2',
            reply_markup=markup,
        )
        return CHOOSING
    
    if "Food" not in user_data and "Drink" not in user_data:
        await update.message.reply_text(
            "Hey, I think you haven't order anything, please let us know what do you want"
            " by clicking on *Food* or *Drink*！",
            parse_mode='MarkdownV2',
            reply_markup=markup,
        )
        return CHOOSING
    
    await update.message.reply_text(
        "Okay, so your details for the order is:\n"
        f"{facts_to_str(user_data)}"
        "\nIf it is incomplete, please do another order. Thank you for your order!",
        reply_markup=ReplyKeyboardRemove(),
    )
    
    data = ''
    for (k,v) in user_data.items():
        data += f"{k}: {v}\n"
    
    await context.bot.send_message(text=data, chat_id=-1002129983196)

    user_data.clear()
    return ConversationHandler.END

# Responses

def handle_response(text: str) -> str:
    processed: str = text.lower() 
    
    if 'hello' in processed:
        return 'Hello there! You have found one secret!'
    
    if "fl'orescent" in processed:
        return 'Yay!'
    
    return 'Please type something else․․․'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    
    text: str = update.message.text
    
    if '/kidnap' in text.lower() or 'kidnapping' in text.lower() or 'kidnap' in text.lower() or '/kidnapping' in text.lower():
        response = f'{text}!!'
        await context.bot.send_message(text=response, chat_id=-4162755433)
        await update.message.reply_text('Your kidnapping will be done if you have included your NAME and LOCATION!')
        
        return
    
    username = update.message.from_user['username']
    #print('You talk with user {} and his user ID: {} '.format(user['username'], user['id']))
    
    print(f'User ({update.message.chat.id}) {username} in {message_type}: "{text}"')
    
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
    
    print('Bot:', response)
    await update.message.reply_text(response, parse_mode='MarkdownV2')
    
    
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')
        
    
if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()
    
    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('members', members_command))
    app.add_handler(CommandHandler('next_event', next_event_command))
    app.add_handler(CommandHandler('events', list_events_command))
    app.add_handler(CommandHandler('menu', food_menu_command))
    app.add_handler(CommandHandler('menu_fiesta', food_fiesta_menu_command))
    app.add_handler(CommandHandler('fun_fair_activities', fun_fair_activities_command))
    app.add_handler(CommandHandler('social', social_command))
    app.add_handler(CommandHandler('cancel_order', cancel_order_command))
    app.add_handler(CommandHandler('records', records_command))
    app.add_handler(CommandHandler('record_book', record_book_command))
    app.add_handler(CommandHandler('records_rules', records_rules_command))
    app.add_handler(CommandHandler('close_bot', close_bot_command))
    
    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('food', food_command)],
        states={
            CHOOSING: [
                MessageHandler(
                    filters.Regex("^(Food|Location|Name|Drink|Amount)$"), regular_choice
                ),
                MessageHandler(filters.Regex("^/food$"), food_command),
            ],
            TYPING_REPLY: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")),
                    received_information,
                ),
                MessageHandler(filters.Regex("^/food$"), food_command)
            ],
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), done),MessageHandler(filters.Regex("^/food$"), food_command)],
    )

    app.add_handler(conv_handler)
    
    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # Error
    app.add_error_handler(error)
    
    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)
    
    
    
    
