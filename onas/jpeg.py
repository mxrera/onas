from steps import StepsFrame
from metrics import snr

class JPEG:
    def __init__(self):
        self.fft_options = {
            "DCT": self.dct,
            "KLT": self.klt,
            "FFT": self.fft
        }
    
    def options(self) -> dict:
        return {
            "Transform": {
                "type": "combobox",
                "values": ["DCT", "KLT", "FFT"],
                "default": "DCT"
            },
            "Quantization Factor": {
                "type": "spinbox",
                "values": [1, 100, 1],
                "default": 1
            },
            "Block Size": {
                "type": "combobox",
                "values": [8, 16, 32, 64, 128],
                "default": 8
            },
        }
    
    def steps(self, steps_parent) -> list:
        return [
            StepsFrame(
                name="Block creation",
                parent=steps_parent,
                description="Divide the image into blocks of the selected size. This helps to divide\
                            the image into more stationary regions, which can be compressed more \
                            efficiently. The block size is usually 8x8, as the improvement in compression \
                            is not significant for larger block sizes",
            ),
            StepsFrame(
                name="Direct Transform",
                parent=steps_parent,
                description="Each block is transformed using the selected method. The optimal transform \
                            is the Karhunen-Loeve Transform (KLT), which base depends on the current image. \
                            However, this will imply sending the base to the receiver, which is not practical. \
                            On the other hand, the Discrete Cosine Transform (DCT) base is fixed and a good \
                            approximation of the KLT and is used in practice (as the bases are known by both \
                            the sender and the receiver we don't need to send them)",
            ),
            StepsFrame(
                name="Quantization",
                parent=steps_parent,
                description="Based on psycho-visual studies, a different quantization step is used \
                            for each transform coefficient. The compression can be controlled by multiplying \
                            the quantization table by a factor, by default 1. The formula applied is: \
                            `^X = round( X / (Q * factor) )`",
            ),
            StepsFrame(
                name="DC coefficient encoding",
                parent=steps_parent,
                description="The DC coefficients, which represent the average color of the block, \
                            are encoded using the difference between the current and the previous block. \
                            This difference is then encoded using Huffman encoding and the DC Huffman table",
            ),
            StepsFrame(
                name="Zig-zag scan",
                parent=steps_parent,
                description="The transformed coefficients are scanned in a zig-zag pattern, so that \
                            the most important coefficients are first and the high-frequency coefficients \
                            are last. This allows for better compression as the high-frequency coefficients \
                            are more likely to be zero and we can use run-length encoding (i.e. End of Block(EOB))",
            ),
            StepsFrame(
                name="AC coefficient encoding",
                parent=steps_parent,
                description="The AC coefficients, which represent the difference between the current \
                            and the previous coefficient, are encoded using Huffman encoding and the AC Huffman table",
            ),
        ]
    
    def configure(self, **kwargs):
        self.fft_algorithm = kwargs.get("Transform", "DCT")
        self.quantization_factor = kwargs.get("Quantization Factor", 1)
        self.block_size = kwargs.get("Block Size", 8)

    def __call__(self, image):
        self.blocks = self.create_blocks(image, self.block_size)
        self.transformed_blocks = self.transform_blocks(self.blocks)
        self.quantized_blocks = self.quantize_blocks(self.transformed_blocks)
        self.encoded_blocks = self.encode_blocks(self.quantized_blocks)
        self.reconstructed_image = self.reconstruct_image(self.encoded_blocks)
        return {
            "image": self.reconstructed_image,
            "snr": snr(image, self.reconstructed_image)
        }

    def create_blocks(self, image, block_size):
        pass

    def transform_blocks(self, blocks):
        return [self.fft_options[self.fft_algorithm](block) for block in blocks]

    def dct(self, block):
        pass

    def klt(self, block):
        pass

    def fft(self, block):
        pass

    def quantize_blocks(self, blocks):
        pass

    def encode_blocks(self, blocks):
        pass

    def reconstruct_image(self, blocks):
        pass
