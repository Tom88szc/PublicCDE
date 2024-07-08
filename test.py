class TLVParser:
    def __init__(self, data):
        self.data = data
        self.parsed_data = {}

    def parse(self):
        index = 0
        while index < len(self.data):
            try:
                tag = self.data[index:index+2]
                length = int(self.data[index+2:index+4])
                value = self.data[index+4:index+4+length]
                self.parsed_data[tag] = value
                index += 4 + length
            except ValueError:
                print(f"Error parsing data at index {index}. Data: {self.data[index:index+10]}")
                break

    def get_parsed_data(self):
        return self.parsed_data

    def display(self):
        for tag, value in self.parsed_data.items():
            print(f"{tag}: {value}")

# Przykład użycia
data = "0104Adam0201A0307Adamski0411Mickiewicza0507Adamowo06030120703POL0807123456090829021980010801011994111191234567890876543212102020013011403POL1508123120251603POL1703POL0214601405BYTOM0602NJ0703POL080520000000950005045BYTOM0502NJ0703POL0322"
parser = TLVParser(data)
parser.parse()
parser.display()
