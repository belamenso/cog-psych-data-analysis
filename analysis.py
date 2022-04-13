from pprint import pprint
from collections import Counter

with open('./data_1.csv') as f:
	read_text = f.read()

data = [line.split(',') for line in read_text.split('\n') if line.strip().__len__()]

assert all(len(x) == 13 for x in data)

# print(data[0])
# ['Age Range', 'Name', 'Last Name', 'Age', 'Sex', 'Nationality', 'Colorblind', 'Induction', 'Color', 'Emotion', 'Mouse Sex', '', 'Comment']

def do_line(line_list):
	return {
		'older':			line_list[data[0].index('Age Range')] == 'Older',      # True/False (True are older ones)
		'colorblind':	line_list[data[0].index('Colorblind')] == 'yes',       # remove if colorblind
		'group':			line_list[data[0].index('Induction')],                 # 'control' 'negative' 'positive'
		'color':			line_list[data[0].index('Color')],
		'emotion':		line_list[data[0].index('Emotion')],
		'comment':		line_list[data[0].index('Comment')].__len__() > 0,     # remove if nonempty
	}

data = [do_line(line) for line in data[1:]]
data = [x for x in data if not x['colorblind'] and not x['comment']]

assert set(x['group'] for x in data) == {'positive', 'negative', 'control'}
assert set(x['color'] for x in data) == {'grey', 'red', 'brown', 'black', 'blue', 'green', 'pink', 'yellow'}
assert set(x['emotion'] for x in data) == {'admiration', 'anger', 'boredom', 'disgust', 'fatigue', 'fear', 'interest', 'joy', 'pride'}

def get_data(group, *, older):
	assert isinstance(older, bool)
	assert group in {'positive', 'negative', 'control'}

	return [x for x in data if x['older'] == older and x['group'] == group]

'''
for b in {True, False}:
	for g in {'positive', 'negative', 'control'}:
		print(g, b, len(get_data(g, older=b)), sep='\t')
'''


experiment_colors = ["red", "blue", "green", "pink", "gray", "yellow", "brown", "black"]

# XXX gray/grey
def same_color(c, c1):
	return c == c1 or ({c, c1} == {'gray', 'grey'})

def get_color_counts(group, *, older):
	_data = get_data(group, older=older)
	return [sum(1 for x in _data if same_color(x['color'], c)) for c in experiment_colors]

for b in {True, False}:
	for g in {'positive', 'negative', 'control'}:
		print('older' if b else 'younger', g, get_color_counts(g, older=b), sep='\t')

print()

for b in {True, False}:
	for g in {'positive', 'negative', 'control'}:
		print('older' if b else 'younger', g, Counter(x['emotion'] for x in get_data(g, older=b)), sep='\t')

