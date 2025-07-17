from plugin import plugin

class velikoSlovo(plugin):
    def getName(self):
        return 'Veliko slovo'

    def getDescription(self):
        return 'Svaku riječ u dokumentu pretvara tako da počinje velikim slovom.'

    def execute(self, model, undoManager, clipboardStack):
        lines = model.getLines()
        capitalizedLines = []
        for l in lines:
            capitalizedWords = []
            words = l.split()
            for w in words:
                capitalizedWords.append(w.capitalize())
            line = ' '.join(capitalizedWords)
            capitalizedLines.append(line)
        model.insertText("\n".join(capitalizedLines) + '\n')
