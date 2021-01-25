class Hash:
    def __init__(self, string):
        self.string = string

    def encrypt(self):
        asc = [ord(ch) for ch in self.string] # Converts each individual character to it's ASCII equivalent
        self.encrypted = [int(ASC) * 2 + len(self.string) for ASC in asc] # Doubles the ASCII equivalent of each character then adds the length of the parent string to it.
         # Joins all the encrypted values with '+' symbols

        string = ""
        for num in self.encrypted:
            if num == self.encrypted[-1]:
                string += str(num)
            else:
                string += f"{str(num)}+" 
        
        
        return string

    def decrypt(self, string = None):
        if string is None:
            string = self.string

        encrypted = string.split("+")
        # Spilts the encrypted values by the '+' symbols.
        reversed = [int((int(ch) - len(encrypted))/2) for ch in encrypted] # Decrypts it.
        decrypted = [chr(asciiCharacter) for asciiCharacter in reversed] # Decrupts it to a string

        return "".join(decrypted) # returns plain text

