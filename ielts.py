import openai
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, JobQueue
import random

# Set your OpenAI API key
openai.api_key = 'your-openai-api-key'

# Predefined topics
topics = [
    "Art", "Business & Money", "Communication & Personality", "Crime & Punishment", "Education",
    "Environment", "Family & Children", "Food & Diet", "Government", "Health",
    "Housing, Buildings & Urban Planning", "Language", "Leisure", "Media & Advertising", "Reading",
    "Society", "Space Exploration", "Sport & Exercise", "Technology", "Tourism and Travel",
    "Transport", "Work"
]

# Predefined IELTS words for each topic with more advanced words for random selection
ielts_words = {
    "Art": ["creativity", "expression", "gallery", "masterpiece", "aesthetic", "sculpture", "canvas", "abstract", "exhibition", "portrait", "landscape", "medium", "technique", "visual", "conceptual", "installation", "museum", "patron", "curator", "avant-garde"],
    "Business & Money": ["investment", "finance", "revenue", "profit", "market", "economy", "entrepreneur", "capital", "commerce", "corporate", "stock", "dividend", "enterprise", "funding", "bankruptcy", "budget", "merger", "acquisition", "trading", "shareholder"],
    "Communication & Personality": ["interaction", "dialogue", "nonverbal", "empathy", "charisma", "assertiveness", "introvert", "extrovert", "networking", "rapport", "interpersonal", "negotiation", "persuasion", "expressive", "receptive", "diplomacy", "feedback", "active listening", "body language", "presentation"],
    "Crime & Punishment": ["justice", "incarceration", "rehabilitation", "deterrence", "criminal", "verdict", "prosecution", "defense", "penalty", "sentence", "parole", "felony", "misdemeanor", "jurisdiction", "forensic", "testimony", "bail", "law enforcement", "recidivism", "legislation"],
    "Education": ["curriculum", "pedagogy", "literacy", "scholarship", "tuition", "syllabus", "institution", "academic", "discipline", "evaluation", "teaching", "learning", "research", "professor", "student", "lecture", "seminar", "exam", "degree", "diploma"],
    "Environment": ["climate", "sustainability", "biodiversity", "ecosystem", "conservation", "pollution", "recycling", "renewable", "deforestation", "habitat", "emissions", "carbon", "greenhouse", "ozone", "ecology", "wildlife", "nature", "organic", "compost", "biodegradable"],
    "Family & Children": ["parenting", "upbringing", "discipline", "bonding", "nurture", "adolescence", "childcare", "sibling", "household", "generation", "dependents", "guardian", "nursery", "adoption", "foster", "kinship", "inheritance", "custody", "divorce", "reconciliation"],
    "Food & Diet": ["nutrition", "calories", "protein", "vitamin", "minerals", "fiber", "organic", "processed", "vegetarian", "vegan", "balanced diet", "cholesterol", "sugar", "metabolism", "intake", "portion", "allergy", "obesity", "malnutrition", "supplements"],
    "Government": ["democracy", "policy", "election", "diplomacy", "legislation", "sovereignty", "campaign", "constitution", "parliament", "senate", "congress", "vote", "party", "law", "rights", "justice", "republic", "state", "authority", "bureaucracy"],
    "Health": ["nutrition", "epidemic", "wellness", "therapy", "diagnosis", "prevention", "hygiene", "vaccine", "clinical", "rehabilitation", "mental", "physical", "healthcare", "medicine", "disease", "treatment", "doctor", "hospital", "surgery", "pharmacy"],
    "Housing, Buildings & Urban Planning": ["architecture", "urbanization", "infrastructure", "zoning", "sustainability", "habitat", "renovation", "construction", "neighborhood", "residential", "commercial", "skyscraper", "landscaping", "blueprint", "density", "public housing", "homelessness", "gentrification", "urban sprawl", "smart city"],
    "Language": ["linguistics", "grammar", "vocabulary", "bilingual", "fluency", "syntax", "dialect", "accent", "phonetics", "semantics", "translation", "interpretation", "idiom", "colloquial", "proficiency", "multilingual", "orthography", "etymology", "morphology", "syntax"],
    "Leisure": ["recreation", "hobby", "pastime", "entertainment", "relaxation", "vacation", "leisurely", "amusement", "activity", "gaming", "craft", "sports", "fitness", "gardening", "traveling", "reading", "photography", "collecting", "volunteering", "meditation"],
    "Media & Advertising": ["journalism", "broadcast", "editorial", "propaganda", "publicity", "campaign", "commercial", "endorsement", "sponsorship", "advertisement", "headline", "circulation", "viewership", "ratings", "subscription", "press release", "digital media", "social media", "influencer", "branding"],
    "Reading": ["literature", "novel", "author", "genre", "fiction", "nonfiction", "poetry", "prose", "bibliography", "publishing", "manuscript", "reading comprehension", "book review", "library", "literacy", "narrative", "plot", "character", "theme", "motif"],
    "Society": ["community", "social", "equality", "justice", "welfare", "diversity", "integration", "norms", "values", "migration", "population", "culture", "ethnicity", "class", "gender", "inclusion", "rights", "responsibility", "interaction", "behavior"],
    "Space Exploration": ["astronomy", "cosmos", "planet", "satellite", "orbit", "telescope", "astronaut", "spacecraft", "galaxy", "comet", "meteor", "universe", "extraterrestrial", "NASA", "mission", "launch", "rover", "spacestation", "astrophysics", "interstellar"],
    "Sport & Exercise": ["athletics", "competition", "fitness", "training", "tournament", "league", "recreation", "exercise", "coach", "team", "game", "match", "score", "goal", "player", "sport", "championship", "stadium", "fans", "strategy"],
    "Technology": ["innovation", "cyberspace", "automation", "digital", "artificial", "intelligence", "internet", "software", "hardware", "development", "network", "programming", "robotics", "cloud", "AI", "blockchain", "data", "cybersecurity", "virtual", "augmented"],
    "Tourism and Travel": ["tourism", "itinerary", "expedition", "adventure", "destination", "journey", "voyage", "excursion", "landscape", "passport", "ticket", "booking", "accommodation", "guide", "tour", "cruise", "flight", "resort", "backpacking", "exploration"],
    "Transport": ["transportation", "infrastructure", "commute", "vehicle", "traffic", "public transit", "logistics", "freight", "automobile", "railway", "aviation", "shipping", "route", "highway", "metro", "bus", "bicycle", "electric", "carpool", "rideshare"],
    "Work": ["employment", "career", "profession", "occupation", "job", "workforce", "recruitment", "salary", "promotion", "internship", "skillset", "resume", "interview", "freelance", "entrepreneur", "corporate", "industry", "sector", "workplace", "productivity"]
}

# Global variable to keep track of the selected topic
selected_topic = None

# Define a function to handle the /start command
def start(update: Update, context: CallbackContext) -> None:
    welcome_message = (
        "Hello! I am your IELTS essay assistant bot. I can help you prepare for the writing part of the IELTS.\n\n”
“Please choose a topic from the list below or press the dice 🎲 to get a random topic.”
)
# Define keyboard layout
keyboard = [
[KeyboardButton(topic) for topic in topics[:5]],
[KeyboardButton(topic) for topic in topics[5:10]],
[KeyboardButton(topic) for topic in topics[10:15]],
[KeyboardButton(topic) for topic in topics[15:20]],
[KeyboardButton(topic) for topic in topics[20:]],
[KeyboardButton(“🎲 Random Topic”)]
]
reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
update.message.reply_text(welcome_message, reply_markup=reply_markup)

Define a function to handle topic selection

def handle_topic(update: Update, context: CallbackContext) -> None:
global selected_topic
user_text = update.message.text
if user_text == “🎲 Random Topic”:
selected_topic = random.choice(topics)
elif user_text in topics:
selected_topic = user_text
else:
update.message.reply_text(“Please choose a valid topic or press the dice 🎲 for a random topic.”)
return
words = random.sample(ielts_words[selected_topic], 10)
word_count = 250  # Assuming an average word count for an IELTS essay
response_message = (
    f"You have selected the topic: {selected_topic}\n\n"
    "Here are 10 IELTS-related words that you should try to include in your essay:\n" +
    "\n".join(f"- {word}" for word in words) +
    f"\n\nYour essay should be around {word_count} words.\n\n"
    "Please write your essay and send it to me for review."
)
update.message.reply_text(response_message)

Define a function to handle essay submission and provide feedback
def handle_essay(update: Update, context: CallbackContext) -> None:
user_essay = update.message.text
response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=(
        f"Provide a detailed IELTS-style assessment for the following essay. "
        f"Assess it based on Task Achievement, Coherence and Cohesion, Lexical Resource, and Grammatical Range and Accuracy.\n\n"
        f"Essay: {user_essay}"
    ),
    max_tokens=500
)
feedback = response.choices[0].text.strip()
update.message.reply_text(f"Here is your feedback:\n\n{feedback}")
Define a function to send practice reminders every 4 hours

def send_practice_reminder(context: CallbackContext) -> None:
job = context.job
context.bot.send_message(job.context, text=“It’s time to practice your IELTS essay writing! Choose a new topic or review your previous work.”)

def set_reminders(update: Update, context: CallbackContext) -> None:
chat_id = update.message.chat_id
context.job_queue.run_repeating(send_practice_reminder, interval=14400, first=10, context=chat_id)
update.message.reply_text(“Practice reminders set! You’ll receive a reminder every 4 hours to practice your IELTS essay writing.”)

def main() -> None:
# Set your Telegram bot token
updater = Updater(‘your-telegram-bot-token’)
dispatcher = updater.dispatcher
job_queue = updater.job_queue

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_topic))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_essay))
dispatcher.add_handler(CommandHandler("set_reminders", set_reminders))

# Start the Bot
updater.start_polling()
updater.idle()
if name == ‘main’:
main()