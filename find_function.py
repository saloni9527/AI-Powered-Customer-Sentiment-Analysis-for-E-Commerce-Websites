with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines, start=1):
    if 'def get_all_sentiment_words' in line:
        print(f'Found at line {i}')
        break
else:
    print('Function not found')
