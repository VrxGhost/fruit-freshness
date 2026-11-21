# Fruit Freshness Checker

Classifies a photo of an apple, banana or orange as **fresh or rotten** with a MobileNetV2 model that runs **entirely in the browser**. No server is involved, and the photo never leaves the device.

**Live demo:** https://vrxghost.github.io/fruit-freshness/

It supports **SDG 2** (Zero Hunger), **SDG 13** (Climate Action) and **SDG 3** (Good Health and Well-being).

## What the app shows

1. **Input:** the photo, uploaded or taken with the camera.
2. **Preprocessing:** the 224 × 224 image the model receives (resize to 256, centre crop, ImageNet normalisation).
3. **Prediction:** softmax probabilities for all six classes.
4. **Output:** a verdict (*OK to distribute*, *remove from supply*, or *uncertain* below 70% confidence) and a Grad-CAM heatmap showing where the model looked.

## Results (leak-free test set, 2,007 images)

| Model | Accuracy | Macro F1 | Rotten recall |
|---|---|---|---|
| MobileNetV2 (transfer learning) | 99.50% | 0.9947 | 99.65% |
| Custom CNN (from scratch) | 90.03% | 0.9037 | 97.20% |

The Kaggle dataset's 13,599 images come from only 1,511 photographs (9 versions each), and 100% of its provided test images had a version in the training set. We therefore re-split the data by original photograph before evaluating.

## How it works

- **Training:** PyTorch, MobileNetV2 pretrained on ImageNet, fine-tuned in two phases on Google Colab (Tesla T4).
- **Export:** the model is exported to ONNX (`model/fruit_freshness.onnx`, 9.1 MB). It outputs class probabilities and a 7 × 7 class activation map per class. For a global-pooling + linear head this map is identical to Grad-CAM, so no gradients are needed in the browser.
- **Inference:** ONNX Runtime Web (WebAssembly) runs the model on the visitor's device.

## Run it locally

A browser cannot load the model from a double-clicked file, so start a small local server:

```bash
python -m http.server 8000
# then open http://localhost:8000
```

### Offline (no internet at all)

Run this once while online. It downloads ONNX Runtime into `ort/`:

```bash
python get_offline_files.py
```

After that, `python -m http.server 8000` works with the internet switched off.

## Project structure

```
index.html                  the app (HTML, CSS and JavaScript in one file)
model/fruit_freshness.onnx  trained MobileNetV2 exported to ONNX
samples/                    six sample images from the dataset
get_offline_files.py        downloads ONNX Runtime for offline use
```

## Limitations

- Trained only on apples, bananas and oranges, one fruit per photo.
- Any image, even a non-fruit, is forced into one of six classes; the 70% threshold reduces but does not remove this.
- Training images are clean close-ups, so cluttered or poorly lit real-world photos may score lower.
- A prototype, not a certified food-safety tool.

## Credits

- Dataset: S. R. Kalluri, [Fruits fresh and rotten for classification](https://www.kaggle.com/datasets/sriramr/fruits-fresh-and-rotten-for-classification), Kaggle.
- M. Sandler et al., "MobileNetV2: Inverted residuals and linear bottlenecks," CVPR 2018.
- R. R. Selvaraju et al., "Grad-CAM: Visual explanations from deep networks via gradient-based localization," ICCV 2017.
- [ONNX Runtime Web](https://onnxruntime.ai/docs/tutorials/web/).
