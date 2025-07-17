import ast
import re


def eval_expression(exp, variables={}):
  def _eval(node):
    if isinstance(node, ast.Num):
      return node.n
    elif isinstance(node, ast.Name):
      return variables[node.id]
    elif isinstance(node, ast.BinOp):
      return _eval(node.left) + _eval(node.right)
    else:
      raise Exception('Unsupported type {}'.format(node))

  node = ast.parse(exp, mode='eval')
  return _eval(node.body)


class Cell:
    def __init__(self, ref, sheet):
        self.ref = ref
        self.sheet = sheet
        self.exp = "0"
        self.value = 0
        self.oldreferences = []
        self.dependentcells = []

    def updatecalculator(self, possiblecycle=None):

        if possiblecycle is None:
            possiblecycle = set()
        if self.ref in possiblecycle:
            raise RuntimeError('Cycle detected!')
        possiblecycle.add(self.ref)

        newreferences = self.sheet.getrefs(self)
        for newref in newreferences:
            if self in self.sheet.cell(newref).oldreferences:
                raise RuntimeError('Cycle detected!')

        for cell in self.oldreferences:
            cell.dependentcells.remove(self)

        self.oldreferences = []

        for newref in newreferences:
            cell = self.sheet.cell(newref)
            self.oldreferences.append(cell)
            cell.dependentcells.append(self)

        self.value = self.sheet.evaluate(self)

        for cell in self.dependentcells:
            cell.updatecalculator(possiblecycle)


class Sheet:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        cells = []
        for i in range(rows):
            row = []
            for j in range(columns):
                row.append(Cell(chr(ord('A') + i) + str(j + 1), self))
            cells.append(row)
        self.cells = cells

    def cell(self, ref):
        i = 0
        for red in self.cells:
            j = 0
            for cell in red:
                if cell.ref == ref:
                    return self.cells[i][j]
                j = j + 1
            i = i + 1
        return 'No ref'

    def set(self, ref, content):
        cell = self.cell(ref)
        cell.exp = content
        cell.updatecalculator()

    def getrefs(self, cell):
        referenceslist = re.findall(r'[A-Z][0-9]+', cell.exp)
        return referenceslist

    def evaluate(self, cell):
        referenceslist = self.getrefs(cell)
        variables = {}
        for ref in referenceslist:
            variables[ref] = self.cell(ref).value
        return eval_expression(cell.exp, variables)

    def print(self):
        for row in self.cells:
            onerow = []
            for cell in row:
                onerow.append(str(cell.value))
            onerow = " ".join(onerow)
            print(onerow)

    def printref(self):
        for row in self.cells:
            onerow = []
            for cell in row:
                onerow.append(cell.ref)
            onerow = " ".join(onerow)
            print(onerow)

    def printexp(self):
        for row in self.cells:
            onerow = []
            for cell in row:
                onerow.append(cell.exp)
            onerow = " ".join(onerow)
            print(onerow)


if __name__ == "__main__":
    s = Sheet(5, 5)
    s.printref()
    print('===================================')

    s.set('A1', '2')
    print('A1 -> 2')
    s.printexp()
    print()
    s.print()
    print('===================================')
    s.set('A2', '5')
    print('A2 -> 5')
    s.printexp()
    print()
    s.print()
    print('===================================')
    s.set('A3', 'A1+A2')
    print('A3 -> A1+A2')
    s.printexp()
    print()
    s.print()
    print('===================================')

    c = s.cell('A3')
    reference = s.getrefs(c)
    print('A3 referncira:', reference)
    print('===================================')

    s.set('A1', '4')
    print('A1 -> 4')
    s.printexp()
    print()
    s.print()
    print('===================================')
    s.set('A4', 'A1+A3')
    print('A4 -> A1+A3')
    s.printexp()
    print()
    s.print()
    print('===================================')
    try:
        print('A1 -> A3')
        s.set('A1', 'A3')
    except RuntimeError as e:
        print("Caught exception:", e)
    s.print()
    print()
    print('===================================')
    s.set('B1', 'B3')
    print('B1 -> B3')
    s.printexp()
    print()
    s.print()
    print('===================================')
    s.set('B3', 'B4')
    print('B3 -> B4')
    s.printexp()
    print()
    s.print()
    print('===================================')
    try:
        print('B4 -> B1')
        s.set('B4', 'B1')
    except RuntimeError as e:
        print("Caught exception:", e)
    s.printexp()
    print()
    s.print()
    print('===================================')


