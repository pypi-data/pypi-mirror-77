from .. import ImageResizer
from tests.unit.executors.crafters.image import JinaImageTestCase


class ImageResizerTestCase(JinaImageTestCase):
    def test_resize(self):
        img_width = 20
        img_height = 17
        output_dim = 71
        crafter = ImageResizer(target_size=output_dim)
        img_array = self.create_random_img_array(img_width, img_height)
        crafted_doc = crafter.craft(img_array)
        assert min(crafted_doc['blob'].shape[:-1]) == output_dim
