import efficientnet.tfkeras
from tensorflow.keras.models import load_model
import os
from PIL import Image
import torch
import torch.nn.functional as F
import torchvision.transforms.functional as TF
import numpy as np
from model import PConvUNet
import cv2
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'


class Restoration:
    def __init__(self, seg_model_path="./patch_detection.h5",
                 restore_model_path="./pretrained_pconv.pth"):
        self.seg_model_path = seg_model_path
        self.restore_model_path = restore_model_path

        self.seg_model = load_model(seg_model_path, compile=False)

    def get_segmented_image(self, img_path="./temp/input.png"):
        patched_img = cv2.imread(img_path)
        # cv2_imshow(patched_img)

        patched_img = cv2.resize(patched_img, (256, 256))
        # cv2_imshow(patched_img)

        patched_img = patched_img.reshape(1, 256, 256, 3)
        segmented_img = self.seg_model.predict(patched_img)
        final = (segmented_img.reshape(256, 256) * 256).astype(np.uint8)
        cv2.imwrite('./temp/patched.png', final)
        segmented_img = segmented_img.reshape(256, 256)
        # plt.imshow(segmented_img)

        segmented_neg_img = segmented_img.max() - segmented_img
        # plt.imshow(segmented_neg_img)

        segmented_neg_img[segmented_neg_img > segmented_neg_img.mean()] = 1
        segmented_neg_img[segmented_neg_img < segmented_neg_img.mean()] = 0

        segmented_neg_img = segmented_neg_img * 255
        # print(segmented_neg_img.shape)
        # plt.imshow(segmented_neg_img)
        cv2.imwrite("./temp/temp_mask.jpg", segmented_neg_img)

        return True

    def restore(self, img, mask, resize=False, gpu_id=0):
        # Define the used device
        # device = torch.device(f"cuda:{gpu_id}" if torch.cuda.is_available() else "cpu")
        device = torch.device(f"cpu")

        # Define the model
        # print("Loading the Model...")
        model = PConvUNet(finetune=False, layer_size=7)
        model.load_state_dict(torch.load(self.restore_model_path, map_location=device)['model'])
        model.to(device)
        model.eval()

        # Loading Input and Mask
        # print("Loading the inputs...")
        org = Image.open(img)
        org = TF.to_tensor(org.convert('RGB'))
        mask = Image.open(mask)
        mask = TF.to_tensor(mask.convert('RGB'))
        inp = org * mask

        # Model prediction
        # print("Model Prediction...")
        with torch.no_grad():
            inp_ = inp.unsqueeze(0).to(device)
            mask_ = mask.unsqueeze(0).to(device)
            if resize:
                org_size = inp_.shape[-2:]
                inp_ = F.interpolate(inp_, size=256)
                mask_ = F.interpolate(mask_, size=256)
            raw_out, _ = model(inp_, mask_)
        if resize:
            raw_out = F.interpolate(raw_out, size=org_size)

        # Post process
        raw_out = raw_out.to(torch.device('cpu')).squeeze()
        raw_out = raw_out.clamp(0.0, 1.0)
        out = mask * inp + (1 - mask) * raw_out

        # Saving an output image
        # print("Saving the output...")
        out = TF.to_pil_image(out)
        # img_name = img.split('/')[-1]
        # out.save(os.path.join("examples", "out_{}".format(img_name)))

        return out

    def give_result(self, unrestored_img_path='./temp/input.png', masked_img_path="./temp/temp_mask.jpg"):
        self.get_segmented_image(unrestored_img_path)
        restored_img = self.restore(unrestored_img_path, masked_img_path)
        restored_img = np.asarray(restored_img)
        cv2.imwrite("./temp/restored.png", cv2.cvtColor(restored_img, cv2.COLOR_BGR2RGB))
        return "True"
