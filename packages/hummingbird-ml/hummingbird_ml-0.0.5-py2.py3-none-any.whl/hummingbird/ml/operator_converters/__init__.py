# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
All operators converters are stored under this package.
"""

# Register constants used within Hummingbird converters.
from . import constants as converter_constants
from .. import supported as hummingbird_constants
from .._utils import _Constants

# Add constants in scope.
constants = _Constants(converter_constants, hummingbird_constants)

# To register a converter for scikit-learn API operators, import associated modules here.
from .onnx import onnx_operator  # noqa: E402
from .onnx import onnxml_array_feature_extractor  # noqa: E402
from .onnx import onnxml_linear  # noqa: E402
from .onnx import onnxml_normalizer  # noqa: E402
from .onnx import onnxml_one_hot_encoder  # noqa: E402
from .onnx import onnxml_scaler  # noqa: E402
from .onnx import onnxml_tree_ensemble  # noqa: E402
from .sklearn import lightgbm  # noqa: E402
from .sklearn import skl_array_feature_extractor  # noqa: E402
from .sklearn import skl_decision_tree  # noqa: E402
from .sklearn import skl_gbdt  # noqa: E402
from .sklearn import skl_iforest  # noqa: E402
from .sklearn import skl_linear  # noqa: E402
from .sklearn import skl_normalizer  # noqa: E402
from .sklearn import skl_one_hot_encoder  # noqa: E402
from .sklearn import skl_scaler  # noqa: E402
from .sklearn import skl_sv  # noqa: E402
from .sklearn import xgb  # noqa: E402


__pdoc__ = {}
__pdoc__["hummingbird.operator_converters._array_feature_extractor_implementations"] = True
__pdoc__["hummingbird.operator_converters._gbdt_commons"] = True
__pdoc__["hummingbird.operator_converters._linear_implementations"] = True
__pdoc__["hummingbird.operator_converters._normalizer_implementations"] = True
__pdoc__["hummingbird.operator_converters._one_hot_encoder_implementations"] = True
__pdoc__["hummingbird.operator_converters._scaler_implementations"] = True
__pdoc__["hummingbird.operator_converters._tree_commons"] = True
__pdoc__["hummingbird.operator_converters._tree_implementations"] = True
