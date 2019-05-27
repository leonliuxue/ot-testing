import xlrd

class readExcel(object):
    def __init__(self, path):
        self.path = path

    @property
    def getSheet(self):
        # 获取索引
        xl = xlrd.open_workbook(self.path)
        sheet = xl.sheet_by_index(0)
        return sheet

    @property
    def getRows(self):
        # 获取行数
        rows = self.getSheet.nrows
        return rows

    @property
    def getCol(self):
        # 获取列数
        col = self.getSheet.ncols
        return col

    # 以下是分别获取每一列的数值
    def getName(self, column_index):
        if column_index <= self.getCol:
            ColumnName = []
            for i in range(1, self.getRows):
                ColumnName.append(self.getSheet.cell_value(i, column_index))
            return ColumnName
        else:
            print("输入的column不合法！")