import math
import numpy as np

from steps import StepsFrame
from metrics import psnr

from scipy.fftpack import dct, idct
import matplotlib.pyplot as plt

class JPEG:
    def __init__(self):
        self.dft_options = {
            "DCT": self.dct,
            "KLT": self.klt,
            "FFT": self.fft
        }
        self.idft_options = {
            "DCT": self.inverse_dct,
            "KLT": self.inverse_klt,
            "FFT": self.inverse_fft
        }
        self.quantization_table = [
            [16, 11, 10, 16, 24, 40, 51, 61],
            [12, 12, 14, 19, 26, 58, 60, 55],
            [14, 13, 16, 24, 40, 57, 69, 56],
            [14, 17, 22, 29, 51, 87, 80, 62],
            [18, 22, 37, 56, 68, 109, 103, 77],
            [24, 35, 55, 64, 81, 104, 113, 92],
            [49, 64, 78, 87, 103, 121, 120, 101],
            [72, 92, 95, 98, 112, 100, 103, 99]
        ]
        self.codification_steps = []
    
    def options(self) -> dict:
        return {
            "Transform": {
                "type": "combobox",
                "values": ["DCT", "KLT", "FFT"],
                "default": "DCT"
            },
            "Quantization Factor": {
                "type": "slider",
                "values": [1, 100, 1],
                "default": 1
            },
            "Block Size": {
                "type": "combobox",
                "values": ["8", "16", "32", "64", "128"],
                "default": "8"
            },
        }
    
    def steps(self, steps_parent) -> list:
        """
        Create the steps for the JPEG compression algorithm. The steps are
        described in a list of StepsFrame objects that can be displayed in
        the GUI.

        Args:
            steps_parent: The parent frame to place the steps
        Returns:
            A list of StepsFrame objects
        """

        self.codification_steps = [ 
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
        return self.codification_steps
    
    def configure(self, **kwargs) -> None:
        """
        Configure the JPEG compression algorithm with the selected options
        
        Args:
            **kwargs: The selected options
        """
        self.fft_algorithm = str(kwargs.get("Transform", "DCT"))
        self.quantization_factor = int(kwargs.get("Quantization Factor", 1))
        self.block_size = int(kwargs.get("Block Size", "8"))
    
    def is_standard(self):
        """
        Check if the selected transform is the Discrete Cosine Transform (DCT),
        so that the image can be saved.

        Returns:
            True if the transform is DCT, False otherwise
        """
        return self.fft_algorithm == "DCT" and self.block_size == 8

    def __call__(self, image) -> dict:
        """
        Main method to do the JPEG compression

        Args:
            image: The image to compress
        Returns:
            A dictionary with the reconstructed image, the encoded image and
            the metrics
        """
        blocks = self.create_blocks(image, self.block_size)
        transformed_blocks = self.transform_blocks(blocks)
        quantized_blocks = self.quantize_blocks(transformed_blocks)
        encoded_image = self.encode(quantized_blocks)
        reconstructed_image = self.decode_image(quantized_blocks, image.shape)
        
        return {
            "image": reconstructed_image,
            "data": encoded_image,
            "metrics": {
                "PSNR (dB)": psnr(image, reconstructed_image)
            }
        }

    def create_blocks(self, image, block_size):
        """
        Create blocks of the specified size from the image

        Args:
            image: The image to divide into blocks
            block_size: The size of the blocks
        Returns:
            A list of blocks
        """
        blocks = []
        for i in range(0, image.shape[0], block_size):
            for j in range(0, image.shape[1], block_size):
                blocks.append(image[i:i+block_size, j:j+block_size])

        # Display the blocks                        
        for i in range(9):
            plot = self.codification_steps[0].get_plot(3, 3, i+1)
            plot.imshow(blocks[len(blocks)//2 + i], cmap='gray')
            plot.axis('off')
        self.codification_steps[0].update_plot()
        
        return blocks

    def transform_blocks(self, blocks):
        """
        Transform the blocks using the selected algorithm

        Args:
            blocks: The blocks to transform
        Returns:
            The transformed blocks
        """
        transformed_blocks = [self.dft_options[self.fft_algorithm](block) for block in blocks]

        # Display the transformed blocks
        for i in range(9):
            plot = self.codification_steps[1].get_plot(3, 3, i+1)
            plot.imshow(transformed_blocks[len(transformed_blocks)//2 + i], cmap='gray')
            plot.axis('off')
        self.codification_steps[1].update_plot()

        return transformed_blocks

    def inverse_transform_blocks(self, blocks):
        """
        Inverse transform the blocks using the selected algorithm

        Args:
            blocks: The transformed blocks
        Returns:
            The untransformed blocks
        """
        return [self.idft_options[self.fft_algorithm](block) for block in blocks]

    def dct(self, block):
        """
        Apply the Discrete Cosine Transform to the block.

        The DCT is the most commonly used transform for image compression, 
        as it is energypreserving and the coefficients are real numbers. 
        The DCT is used in JPEG compression.

        Args:
            block: The block to transform
        Returns:
            The transformed block
        """
        m, n = self.block_size, self.block_size
        dct = [[ 0 for _ in range(n)] for _ in range(m)]
        pi = math.pi
        
        for i in range(m):
            for j in range(n):
                if (i == 0):
                    ci = 1 / (m ** 0.5)
                else:
                    ci = (2 / m) ** 0.5
                if (j == 0):
                    cj = 1 / (n ** 0.5)
                else:
                    cj = (2 / n) ** 0.5
        
                sum = 0
                for k in range(m):
                    for l in range(n):
                    
                        dct1 = block[k][l] * math.cos((2 * k + 1) * i * pi / (
                        2 * m)) * math.cos((2 * l + 1) * j * pi / (2 * n))
                        sum = sum + dct1
 
                dct[i][j] = ci * cj * sum

        return dct
        # return dct(dct(block, axis=0, norm='ortho'), axis=1, norm='ortho')
    
    def inverse_dct(self, transformed_block):
        """
        Apply the Inverse Discrete Cosine Transform to the block.

        Args:
            block: The transformed block
        Returns:
            The untransformed block
        """
        return idct(idct(transformed_block, axis=0, norm='ortho'), axis=1, norm='ortho')

    def klt(self, block):
        """
        Apply the Karhunen-Loeve Transform to the block.

        The KLT is the optimal transform for a given image, as it minimizes the energy
        of the coefficients. However, the KLT is not used in practice as the base depends
        on the image and needs to be sent to the receiver. 
        
        If KLT is selected the image cannot be saved as the bases are not known.

        Args:
            block: The block to transform
        Returns:
            The transformed block
        """
        ...

    def inverse_klt(self, transformed_block):
        """
        Apply the Inverse Karhunen-Loeve Transform to the block.

        Args:
            block: The transformed block
        Returns:
            The untransformed block
        """
        ...    

    def fft(self, block):
        """
        Apply the Fast Fourier Transform to the block.

        Note that using the FFT is not the best option for image compression, as the FFT
        is not energy preserving and the coefficients are complex numbers. However, it is
        a good option for demonstration purposes.

        Args:
            block: The block to transform
        Returns:
            The transformed block
        """
        ...

    def inverse_fft(self, transformed_block):
        """
        Apply the Inverse Fast Fourier Transform to the block.

        Args:
            block: The transformed block
        Returns:
            The untransformed block
        """
        ...

    def quantize_blocks(self, transformed_blocks):
        """
        Quantize the transformed blocks using the quantization factor. 
        Can only be used with the DCT transform and the standard block size of 8x8.

        Args:
            blocks: The transformed blocks
        Returns:
            The quantized blocks
        """
        if not self.is_standard():
            return transformed_blocks

        for block in transformed_blocks:
            for i in range(len(self.quantization_table)):
                for j in range(len(self.quantization_table[0])):
                    block[i][j] = round(block[i][j] / (self.quantization_factor * self.quantization_table[i][j]))

        # Display the quantized blocks
        for i in range(9):
            plot = self.codification_steps[2].get_plot(3, 3, i+1)
            plot.imshow(transformed_blocks[len(transformed_blocks)//2 + i], cmap='gray')
            plot.axis('off')
        self.codification_steps[2].update_plot()
                
        return transformed_blocks
    
    def unquantize_blocks(self, quantized_blocks):
        """
        Unquantize the quantized blocks using the quantization factor. 
        Can only be used with the DCT transform and the standard block size of 8x8.

        Args:
            quantized_blocks
        Returns:
            The unquantized blocks
        """
        if not self.is_standard():
            return quantized_blocks
        
        for block in quantized_blocks:
            for i in range(len(self.quantization_table)):
                for j in range(len(self.quantization_table[0])):
                    block[i][j] = block[i][j] * (self.quantization_factor * self.quantization_table[i][j])
        
        return quantized_blocks

    def encode(self, blocks):
        """
        Encode the DC and AC coefficients of the image
        """
        if not self.is_standard():
            return None
        ...

    def decode_image(self, encoded_blocks, image_shape):
        """
        Decode the DC and AC coefficients of the image and return the reconstructed image

        Args:
            encoded_blocks: The encoded blocks
            image_shape: The shape of the image
        Returns:
            The reconstructed image
        """
        unquantize_encoded_blocks = self.unquantize_blocks(encoded_blocks)
        untransformed_blocks = self.inverse_transform_blocks(unquantize_encoded_blocks)
        reconstructed_image = np.zeros((image_shape[0], image_shape[1]))
        
        for i in range(0, image_shape[0], self.block_size):
            for j in range(0, image_shape[1], self.block_size):
                reconstructed_image[i:i+self.block_size, j:j+self.block_size] = untransformed_blocks.pop(0)
        
        return reconstructed_image

    def save_image(self, image, filename: str):
        """
        Save the image to the specified filename
        """
        if not self.is_standard():
            raise ValueError("Cannot save image when using a different transform than DCT")
        ...

