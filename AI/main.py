from dotenv import load_dotenv
from Resume_loaders import exatract_pdf
load_dotenv()



text = exatract_pdf("AI/suvi.pdf")

print(text)


