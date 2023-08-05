import pytest

from azureml.contrib.automl.dnn.vision.classification.models.classification_model_wrappers import ModelFactory, \
    Resnet18Wrapper, Mobilenetv2Wrapper, SeresnextWrapper
from azureml.contrib.automl.dnn.vision.classification.common.constants import ModelNames, \
    base_training_settings_defaults
from azureml.contrib.automl.dnn.vision.common.constants import SettingsLiterals
from azureml.automl.core.shared.exceptions import ClientException
from ..common.utils import check_exported_onnx_model
import torch


@pytest.mark.usefixtures('new_clean_dir')
class TestModelWrappers:
    def _load_batch_of_pil(self, test_data_image_list):
        raise NotImplementedError

    def test_wrappers(self):
        # right now only initialization and making sure that the model is working
        Resnet18Wrapper(20)
        Mobilenetv2Wrapper(20)
        SeresnextWrapper(20)

        assert True

    def test_wrappers_export_onnx(self):
        # right now only initialization and making sure that the model is working
        device = base_training_settings_defaults[SettingsLiterals.DEVICE]
        input = torch.rand(1, 3, 224, 224, device=device, requires_grad=False)

        def get_model_output(wrapper, input, device):
            return wrapper._get_model_output(input)

        res18 = Resnet18Wrapper(20)
        res18_file = 'Resnet18Wrapper.onnx'
        res18.export_onnx_model(file_path=res18_file, device=device)
        check_exported_onnx_model(res18_file, res18, input, device, get_model_output, True)

        mv2 = Mobilenetv2Wrapper(20)
        mv2_file = 'Mobilenetv2Wrapper.onnx'
        mv2.export_onnx_model(file_path=mv2_file, device=device)
        check_exported_onnx_model(mv2_file, mv2, input, device, get_model_output, True)

        sn = SeresnextWrapper(20)
        sn_file = 'SeresnextWrapper.onnx'
        sn.export_onnx_model(file_path=sn_file, device=device)
        check_exported_onnx_model(sn_file, sn, input, device, get_model_output, True)
        # export onnx w/ normalization
        snn_file = 'SeresnextWrapperNorm.onnx'
        sn.export_onnx_model(file_path=snn_file, device=device, enable_norm=True)
        check_exported_onnx_model(snn_file, sn, input, device, get_model_output, False)

        assert True

    def test_model_factory(self):
        ModelFactory.get_model_wrapper(ModelNames.RESNET18, 5)
        ModelFactory.get_model_wrapper(ModelNames.MOBILENETV2, 5)
        ModelFactory.get_model_wrapper(ModelNames.SERESNEXT, 5)

        assert True

    def test_model_factory_nonpresent_model(self):
        with pytest.raises(ClientException):
            ModelFactory.get_model_wrapper('nonexistent_model')

    @pytest.mark.skip(reason="not implemented")
    def test_model_predict(self):
        raise NotImplementedError

    @pytest.mark.skip(reason="not implemented")
    def test_model_predict_proba(self):
        raise NotImplementedError
