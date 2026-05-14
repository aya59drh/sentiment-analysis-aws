import re

def clean_text(text: str) -> str:
    """Nettoie un post pour le NLP"""
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', '', text)       # URLs
    text = re.sub(r'@\w+', '', text)                  # mentions
    text = re.sub(r'#(\w+)', r'\1', text)             # hashtags (garde le mot)
    text = re.sub(r'[^\w\s]', '', text)               # ponctuation
    text = re.sub(r'\s+', ' ', text).strip()          # espaces multiples
    return text

if __name__ == '__main__':
    tests = [
        "This match is INCREDIBLE! @FIFA #WorldCup2026 https://t.co/abc",
        "Je suis déçu... #Nul @Equipe",
        "   Great goal!!!   🔥🔥🔥  "
    ]
    for t in tests:
        print(f"Avant : {t}")
        print(f"Après : {clean_text(t)}\n")