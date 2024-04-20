
class console:
    maxLen = 10
    curlen = 0
    log = []

    def addElem(self, txt):
        if self.curlen == self.maxLen:
            self.log.pop()
            self.curlen -= 1
        self.log.append(txt)
        self.curlen += 1

    def getLog(self):
        result = ""
        for i in self.log:
            result += i + "\n"
        return result