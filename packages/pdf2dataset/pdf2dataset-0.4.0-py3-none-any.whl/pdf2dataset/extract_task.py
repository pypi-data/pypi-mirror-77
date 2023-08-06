import traceback
from abc import ABC
from copy import deepcopy
from itertools import chain
from inspect import getmembers, isroutine
from functools import wraps

import pyarrow as pa


def feature(pyarrow_type, is_helper=False, exceptions=None):
    exceptions = exceptions or tuple()
    exceptions = tuple(exceptions)

    def decorator(feature_method):
        feature_method.is_feature = True
        feature_method.is_helper = is_helper
        feature_method.pyarrow_type = None

        type_ = getattr(pa, pyarrow_type)()

        if isinstance(type_, pa.DataType):
            feature_method.pyarrow_type = type_
        else:
            raise ValueError(f'Invalid PyArrow type {pyarrow_type}!')

        @wraps(feature_method)
        def inner(*args, **kwargs):
            result, error = None, None

            try:
                result = feature_method(*args, **kwargs)
            except exceptions:
                error = traceback.format_exc()

            return result, error
        return inner

    return decorator


# TODO: Eventually, I'll make this a new lib
class ExtractTask(ABC):

    fixed_featues = ('path')
    _feature_prefix = 'get_'  # Optional

    def __init__(self, path, file_bin=None, sel_features='all'):
        self.path = path
        self.file_bin = file_bin
        self.sel_features = self._parse_sel_features(sel_features)

        self._features = {}
        self._errors = {}

        self._init_all_features()

    @classmethod
    def list_helper_features(cls):
        prefix = cls._feature_prefix

        def is_helper(name, method):
            return (getattr(method, 'is_helper', False)
                    and name.startswith(prefix))

        class_routines = getmembers(cls, predicate=isroutine)

        return [n[len(prefix):] for n, m in class_routines if is_helper(n, m)]

    @classmethod
    def list_features(cls, *, exclude_fixed=True):
        def include(name, method):
            helper_features = [cls._get_feature_methodname(f)
                               for f in cls.list_helper_features()]

            return (getattr(method, 'is_feature', False)
                    and name not in helper_features
                    and name.startswith(cls._feature_prefix)
                    and not (name in cls.fixed_featues and exclude_fixed))

        class_routines = getmembers(cls, predicate=isroutine)

        return [n[len(cls._feature_prefix):]
                for n, m in class_routines if include(n, m)]

    @classmethod
    def get_schema(cls, features=()):
        def get_type(feature_name):
            method_name = cls._get_feature_methodname(feature_name)
            method = getattr(cls, method_name)

            if method.is_helper:
                return None

            return method.pyarrow_type

        class_features = cls.list_features()
        names = (name for name in features if name in class_features)

        features_types = ((name, get_type(name)) for name in names)

        features_types = [(f, t) for f, t in features_types if t is not None]
        features_types.append(('error', pa.string()))

        return pa.schema(features_types)

    def load_bin(self, enforce=False):
        '''
        Loads the file binary

        Should not be called inside its class, as the node running
        this task might not have access to the file in his filesystem
        '''
        if enforce or not self.file_bin:
            self.file_bin = self.path.read_bytes()

    def copy(self):
        return deepcopy(self)

    def is_feature_selected(self, feature):
        return feature in self._features

    def get_feature(self, name):
        extract_method_name = self._get_feature_methodname(name)
        extract_method = getattr(self, extract_method_name)

        if self._features[name] is None and self._errors[name] is None:
            self._features[name], self._errors[name] = extract_method()

        return self._features[name], self._errors[name]

    def process(self):
        if not self.file_bin:
            raise RuntimeError(
                "'file_bin' can't be empty for processing the task!"
            )

        for feature in self._features:
            self._features[feature], _ = self.get_feature(feature)

        self._pop_helper_features()
        self._check_result_fixedfeatures()

        return {**self._features, 'error': self._gen_errors_string()}

    def _init_all_features(self):
        features = chain(self.fixed_featues,
                         self.list_helper_features(), self.sel_features)

        self._features = {f: None for f in features}
        self._errors = deepcopy(self._features)

    def _parse_sel_features(self, sel_features):
        possible_features = self.list_features()

        if sel_features == '':
            sel_features = []

        elif sel_features == 'all':
            sel_features = possible_features

        elif isinstance(sel_features, list):
            ...

        else:
            sel_features = sel_features.split(',')

        failed = (f not in possible_features for f in sel_features)
        if any(failed):
            sel_features = ','.join(sel_features)
            possible_features = ','.join(possible_features)

            raise ValueError(
                f"Invalid feature list: '{sel_features}'"
                f"\nPossible features are: '{possible_features}'"
            )

        return sel_features

    @classmethod
    def _get_feature_methodname(cls, feature_name):
        method_name = cls._feature_prefix + feature_name

        if not hasattr(cls, method_name):
            raise RuntimeError(f"Method '{method_name}' not found!")

        return method_name

    def _pop_helper_features(self):
        for helper in self.list_helper_features():
            self._features.pop(helper)

    def _check_result_fixedfeatures(self):
        for fixed in self.fixed_featues:
            error_msg = f'Missing {fixed} in results'
            assert fixed in self._features, error_msg

    def _gen_errors_string(self):
        features_errors = (f'{f}:\n{e}' for f, e in self._errors.items() if e)
        all_errors = '\n\n\n'.join(features_errors)

        return all_errors or None
