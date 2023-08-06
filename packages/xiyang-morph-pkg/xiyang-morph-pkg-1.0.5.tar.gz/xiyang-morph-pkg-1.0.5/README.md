
Fuzhou Xiyang network technology company, face morph project.

# install:

pip install xiyang-morph-pkg

# install relation packages
dlib >= 19.9.0
numpy >= 1.13.1
scipy >= 0.18.0
opencv-contrib-python>=4.2.0.34


# import package
from xiyang_morph import morph
# param 1: str_img_path 
# param 2: dist_img_path
# param 3：result img save path
morph.morph("../../imgs/test6.jpg", "../../imgs/test7.jpg", "../img/result.jpg")
