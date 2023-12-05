import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
import matplotlib.pyplot as plt
import os

def compare_images(original, restored):
    # Convert images to grayscale
    original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    restored_gray = cv2.cvtColor(restored, cv2.COLOR_BGR2GRAY)

    # Calculate MSE
    mse_value = np.mean((original_gray - restored_gray) ** 2)

    # Calculate PSNR
    psnr_value = psnr(original_gray, restored_gray, data_range=original_gray.max())

    # Calculate SSIM
    ssim_value, _ = ssim(original_gray, restored_gray, full=True)

    return mse_value, psnr_value, ssim_value

def process_and_compare_images(source_path, comparison_folder):
    # Load the source image
    original_image = cv2.imread(source_path)

    # Get a list of all files in the comparison folder
    comparison_files = sorted(os.listdir(comparison_folder))

    # Determine the number of comparison images
    num_images = len(comparison_files)

    # Set up subplots dynamically based on the number of comparison images
    fig, axes = plt.subplots(1, num_images + 1, figsize=(5 * (num_images + 1), 5))
    axes[0].imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
    axes[0].set_title('Source Image')

    for i, comparison_file in enumerate(comparison_files):
        # Load the comparison image
        comparison_image = cv2.imread(os.path.join(comparison_folder, comparison_file))

        # Display the comparison image
        axes[i + 1].imshow(cv2.cvtColor(comparison_image, cv2.COLOR_BGR2RGB))
        axes[i + 1].set_title(comparison_file)

        # Image comparison
        mse_value, psnr_value, ssim_value = compare_images(original_image, comparison_image)

        # Display numerical values
        text_str = f'{comparison_file}\nMSE: {mse_value:.2f}\nPSNR: {psnr_value:.2f} dB\nSSIM: {ssim_value:.4f}'

        # Adjust text position to be directly under the image at its center
        axes[i + 1].text(0.5, -0.25, text_str, transform=axes[i + 1].transAxes,
                        ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

    # Adjust spacing
    plt.subplots_adjust(bottom=0.25)

    # Save the resulting comparison image to the result folder
    result_filename = os.path.join(result_folder_path, 'comparison_result.png')
    plt.savefig(result_filename)

    # Show the plot
    plt.show()

# Example usage
source_image_path = 'GT/GT.png'
comparison_folder_path = 'Source/'
result_folder_path = 'Results/'

# Create the result folder if it doesn't exist
os.makedirs(result_folder_path, exist_ok=True)


process_and_compare_images(source_image_path, comparison_folder_path)
