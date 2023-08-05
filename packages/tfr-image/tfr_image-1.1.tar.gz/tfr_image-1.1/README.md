# TFRimage
An experimental minimal tool to create TFRecords from a **small dataset** of images (few thousand images max). Based on code from [create_tfrecords](https://github.com/kwotsin/create_tfrecords) but adapted to Tensorflow 2.0 with some changes. 

## 📋 Installation
```bash
pip install tfr_image
```

## 💻 Usage
Example of the directory structure: 

    ├── cat_dogs_sample
    │   │── train
    │       │── cat
    │            │── cat1.jpg
    │            │── cat2.jpg
    │       │── dog
    │            │──  dog1.jpg
    │            │── dog2.jpg

Example to create `tfrecords` inside `dataset_dir` directory 
```python
from tfr_image import TFRimage

tool = TFRimage()
tool.create_tfrecords(
    dataset_dir="../cat_dogs_sample/train",
    tfrecord_filename="cat_dogs",
    validation_size=0.2,
    num_shards=2,
)
```

## Other Tools

- [tensorflow-recorder](https://github.com/google/tensorflow-recorder) : Google open source tool for *Big* dataset of images that provides connectivity with Google Cloud Dataflow. 