from typing import List, Union
from enum import Enum

from dateutil import parser

from sktmls import MLSClient, MLSENV, MLSClientError, MLSResponse
from sktmls.datasets import Dataset
from sktmls.components import Component

MLS_MODELS_API_URL = "/api/v1/models"

MODEL_LIBS = ["sklearn", "xgboost", "lightgbm", "rule", "etc"]


class MLModel:
    """
    ML모델 클래스 입니다.
    """

    def __init__(self, **kwargs):
        """
        ## Args

        - kwargs
            - id: (int) ML모델 고유 ID
            - name: (str) ML모델 이름
            - version: (str) ML모델 버전
            - creator: (str) ML모델 생성 계정명
            - description: (str) ML모델 설명
            - model_type: (str) ML모델 타입 (`automl` | `manual`)
            - table: (str) ML모델 테이블
            - model_data: (str) ML모델 데이터
            - status: (`sktmls.models.MLModelStatus`) ML모델 상태
            - created_at: (datetime) 생성일시
            - updated_at: (datetime) 수정일시

        ## Returns
        `sktmls.models.MLModel`
        """
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.version = kwargs.get("version")
        self.description = kwargs.get("description")
        self.creator = kwargs.get("creator")
        self.model_type = kwargs.get("model_type")
        self.table = kwargs.get("table")
        self.model_data = kwargs.get("model_data")
        self.status = kwargs.get("status")
        try:
            self.created_at = parser.parse(kwargs.get("created_at"))
        except TypeError:
            self.created_at = None
        try:
            self.updated_at = parser.parse(kwargs.get("updated_at"))
        except TypeError:
            self.updated_at = None

    def __str__(self) -> str:
        return self.name

    def get(self) -> dict:
        return self.__dict__

    def reset(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class AutoMLModel(MLModel):
    """
    AutoML모델 클래스 입니다.
    """

    def __init__(self, **kwargs):
        """
        ## Args

        - kwargs
            - id: (int) ML모델 고유 ID
            - name: (str) ML모델 이름
            - model_type: (str) ML모델 타입 (`automl` | `manual`)
            - version: (str) ML모델 버전
            - description: (str) ML모델 설명
            - creator: (str) ML모델 생성 계정명
            - status: (`sktmls.models.MLModelStatus`) ML모델 상태
            - model_meta: (dict) ML모델 메타정보
            - components: list(dict) ML모델 컴포넌트
            - dataset_id: (int) ML 데이터셋 고유 ID
            - dataset_name: (str) ML 데이터셋 이름
            - automl_model_info: (dict) AutoML모델 정보

        ## Returns
        `sktmls.models.AutoMLModel`
        """

        super().__init__(**kwargs)
        self.dataset_id = kwargs.get("dataset_id")
        self.dataset_name = kwargs.get("dataset_name")
        self.automl_model_info = kwargs.get("automl_model_info")


class ManualModel(MLModel):
    def __init__(self, **kwargs):
        """
        ## Args

        - kwargs
            - id: (int) ML모델 고유 ID
            - name: (str) ML모델 이름
            - model_type: (str) ML모델 타입 (`automl` | `manual`)
            - version: (str) ML모델 버전
            - description: (str) ML모델 설명
            - creator: (str) ML모델 생성 계정명
            - status: (`sktmls.models.MLModelStatus`) ML모델 상태
            - model_meta: (dict) ML모델 메타정보
            - components: list(dict) ML모델 컴포넌트
            - table: (str) ML모델 테이블
            - model_lib: (str) ML모델 라이브러리
            - model_data: (str) ML모델 데이터
            - features: (str) ML모델에 사용된 피쳐
            - is_enabled: (bool) 활성상태 여부

        ## Returns
        `sktmls.models.ManualModel`
        """

        super().__init__(**kwargs)
        self.model_meta = kwargs.get("model_meta")
        self.components = kwargs.get("components")
        self.model_lib = kwargs.get("model_lib")
        self.features = kwargs.get("features")
        self.is_enabled = kwargs.get("is_enabled")


class MLModelStatus(Enum):
    IN_USE = "IN_USE"
    NOT_IN_USE = "NOT_IN_USE"
    AUTOML_TRAINING = "TRAINING"
    AUTOML_DONE = "DONE"
    AUTOML_FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"


class MLModelClient(MLSClient):
    def __init__(self, env: MLSENV = None, username: str = None, password: str = None):
        """
        ## Args

        - env: (`sktmls.MLSENV`) 접근할 MLS 환경 (`sktmls.MLSENV.DEV`|`sktmls.MLSENV.STG`|`sktmls.MLSENV.PRD`) (기본값: `sktmls.MLSENV.STG`)
        - username: (str) MLS 계정명 (기본값: $MLS_USERNAME)
        - password: (str) MLS 계정 비밀번호 (기본값: $MLS_PASSWORD)

        ## Returns
        `sktmls.models.MLModelClient`

        ## Example

        ```
        ml_model_client = MLModelClient(env=MLSENV.STG, username="mls_account", password="mls_password")
        ```
        """
        super().__init__(env=env, username=username, password=password)

    def create_automl_model(self, dataset: Dataset, name: str, version: str, description: str) -> AutoMLModel:
        """
        AutoML 모델을 생성합니다.

        ## Args

        - dataset: (sktmls.datasets.Dataset) ML 데이터셋
        - name: (str) 생성할 AutoML 모델 이름
        - version: (str) 생성할 AutoML 모델 버전
        - description: (str) 생성할 AutoML 설명

        ## Returns
        `sktmls.models.AutoMLModel`

        - name: (str) ML모델 이름
        - model_type: (str) ML모델 타입 (`automl` | `manual`)
        - version: (str) ML모델 버전
        - creator: (str) ML모델 생성 계정명
        - description: (str) ML모델 설명
        - status: (`sktmls.models.MLModelStatus`) ML모델 상태
        - model_meta: (dict) ML모델 메타정보
        - components: list(dict) ML모델 컴포넌트
        - dataset_id: (int) ML 데이터셋 고유 ID
        - dataset_name: (str) ML 데이터셋 이름
        - automl_model_info: (dict) AutoML모델 정보

        ## Example

        ```
        automl_model = ml_model_client.create_automl_model(
            dataset=dataset,
            name="automl_test_model",
            version="v1",
            description='test_model'
        )
        ```
        """
        assert type(dataset) == Dataset

        data = {
            "model_type": "automl",
            "name": name,
            "version": version,
            "description": description,
            "dataset_id": dataset.id,
        }
        response = self._request(method="POST", url=MLS_MODELS_API_URL, data=data).results
        return self.get_automl_model(id=response.get("id"))

    def create_manual_model(
        self,
        name: str,
        version: str,
        description: str = None,
        creator: str = None,
        model_lib: str = None,
        model_data: str = None,
        model_meta: dict = None,
        features: str = None,
        table: str = None,
        components: List[Component] = None,
    ) -> ManualModel:
        """
        일반 모델을 생성합니다.

        ## Args

        - name: (str) 생성할 일반 모델 이름
        - version: (str) 생성할 일반 모델 버전
        - description: (optional) (str) 생성할 일반 모델 설명
        - creator: (optional) (str) 일반 모델 생성 계정명
        - model_lib: (optional) (str) 일반 모델 라이브러리
        - model_data: (optional) (str) 일반 모델 데이터
        - model_meta: (optional) (dict) 모델 레지스트리에 등록된 메타정보(model.json)
        - features: (optional) (str) 일반 모델에 사용된 피쳐
        - table: (optional) (str) 일반 모델 테이블
        - components: (optional) list(`sktmls.components.Component`) 일반 모델 컴포넌트 리스트

        ## Returns
        `sktmls.models.ManualModel`

        - id: (int) ML모델 고유 ID
        - name: (str) ML모델 이름
        - model_type: (str) ML모델 타입 (`automl` | `manual`)
        - version: (str) ML모델 버전
        - description: (str) ML모델 설명
        - creator: (str) ML모델 생성 계정명
        - status: (`sktmls.models.MLModelStatus`) ML모델 상태
        - model_meta: (dict) ML모델 메타정보
        - components: list(dict) ML모델 컴포넌트
        - table: (str) ML모델 테이블
        - model_lib: (str) ML모델 라이브러리
        - model_data: (str) ML모델 데이터
        - features: (str) ML모델에 사용된 피쳐
        - is_enabled: (bool) 활성상태 여부

        ## Example

        ```
        component_1 = component_client.get_component(name="test_component_1")
        component_2 = component_client.get_component(name="test_component_2")
        manual_model = ml_model_client.create_manual_model(
            name="manual_test_model",
            version="v1",
            description="test_model",
            creator="mls_user",
            model_lib="lightgbm",
            model_data="/models/manual_test_model/v1/model.joblib",
            model_meta={
                "name": "manual_test_model",
                "version": "v1",
                "model_lib": "lightgbm",
                "model_lib_version": "2.3.1",
                "model_data": "/models/manual_test_model/v1/model.joblib",
                "features": ["age", "app_use_traffic_youtube", "svc_scrb_period"],
            },
            features="age,app_use_traffic_youtube,svc_scrb_period",
            table="test_model_table",
            components=[component_1, component_2]
        )
        ```
        """

        data = {
            "model_type": "manual",
            "name": name,
            "version": version,
        }
        if description:
            data["description"] = description
        if creator:
            data["creator"] = creator
        if model_lib:
            assert model_lib in MODEL_LIBS, "허용되지 않는 `model_lib`값입니다."
            data["model_lib"] = model_lib
        if model_data:
            data["model_data"] = model_data
        if model_meta:
            data["model_meta"] = model_meta
        if features:
            data["features"] = features
        if table:
            data["table"] = table
        if components:
            for component in components:
                assert type(component) == Component, "`components`는 list(`sktmls.components.Component`) 형태여야 합니다."
            data["components"] = [component.name for component in components]

        response = self._request(method="POST", url=MLS_MODELS_API_URL, data=data).results
        return self.get_manual_model(id=response.get("id"))

    def list_ml_models(self, **kwargs) -> List[MLModel]:
        """
        ML모델 리스트를 가져옵니다.

        ## Args

        - kwargs: (optional) (dict) 필터 조건
            - id: (int) ML모델 고유 ID
            - name: (str) ML모델 이름
            - version: (str) ML모델 이름

        ## Returns
        list(`sktmls.models.MLModel`)

        - id: (int) ML모델 고유 ID
        - name: (str) ML모델 이름
        - version: (str) ML모델 버전
        - creator: (str) ML모델 생성 계정명
        - model_type: (str) ML모델 타입 (`automl` | `manual`)
        - table: (str) ML모델 테이블
        - model_data: (str) ML모델 데이터
        - status: (`sktmls.models.MLModelStatus`) ML모델 상태
        - created_at: (datetime) 생성일시
        - updated_at: (datetime) 수정일시

        ## Example

        ```
        ml_models = ml_model_client.list_ml_models()
        ```
        """
        response = self._request(method="GET", url=MLS_MODELS_API_URL, params=kwargs)
        return [MLModel(**ml_model) for ml_model in response.results]

    def get_automl_model(self, id: int = None, name: str = None, version: str = None) -> AutoMLModel:
        """
        AutoML모델 정보를 가져옵니다.

        ## Args: `id` 또는 (`name` and `version`) 중 한 개 이상의 값이 반드시 전달되어야 합니다.

        - id: (int) ML모델 고유 ID
        - name: (str) ML모델 이름
        - version: (str) ML모델 이름

        ## Returns
        `sktmls.models.AutoMLModel`

        - id: (int) ML모델 고유 ID
        - name: (str) ML모델 이름
        - model_type: (str) ML모델 타입 (`automl` | `manual`)
        - version: (str) ML모델 버전
        - description: (str) ML모델 설명
        - creator: (str) ML모델 생성 계정명
        - status: (`sktmls.models.MLModelStatus`) ML모델 상태
        - model_meta: (dict) ML모델 메타정보
        - components: list(dict) ML모델 컴포넌트
        - dataset_id: (int) ML 데이터셋 고유 ID
        - dataset_name: (str) ML 데이터셋 이름
        - automl_model_info: (dict) AutoML모델 정보

        ## Example

        ```
        ml_model_by_id = ml_model_client.get_automl_model(id=3)
        ml_model_by_name_and_version = ml_model_client.get_automl_model(name="my_automl_model", version="my_automl_version")
        ```
        """
        assert id or (name and version), "`id` 또는 (`name`, `version`) 중 한 개 이상의 값이 반드시 전달되어야 합니다."

        ml_models = self.list_ml_models(id=id, name=name, version=version)
        if len(ml_models) == 0:
            raise MLSClientError(code=404, msg="ML모델이 없습니다.")
        elif len(ml_models) > 1:
            raise MLSClientError(code=409, msg="같은 이름의 모델이 여러개 존재합니다.")

        if ml_models[0].model_type != "automl":
            raise MLSClientError(code=400, msg="AutoML 모델이 아닙니다.")

        return AutoMLModel(**self._request(method="GET", url=f"{MLS_MODELS_API_URL}/{ml_models[0].id}").results)

    def get_manual_model(self, id: int = None, name: str = None, version: str = None) -> ManualModel:
        """
        일반 모델 정보를 가져옵니다.

        ## Args: `id` 또는 (`name` and `version`) 중 한 개 이상의 값이 반드시 전달되어야 합니다.

        - id: (int) ML모델 고유 ID
        - name: (str) ML모델 이름
        - version: (str) ML모델 이름

        ## Returns
        `sktmls.models.ManualModel`

        - id: (int) ML모델 고유 ID
        - name: (str) ML모델 이름
        - model_type: (str) ML모델 타입 (`automl` | `manual`)
        - version: (str) ML모델 버전
        - description: (str) ML모델 설명
        - creator: (str) ML모델 생성 계정명
        - status: (`sktmls.models.MLModelStatus`) ML모델 상태
        - model_meta: (dict) ML모델 메타정보
        - components: list(dict) ML모델 컴포넌트
        - table: (str) ML모델 테이블
        - model_lib: (str) ML모델 라이브러리
        - model_data: (str) ML모델 데이터
        - features: (str) ML모델에 사용된 피쳐
        - is_enabled: (bool) 활성상태 여부

        ## Example

        ```
        ml_model_by_id = ml_model_client.get_manual_model(id=3)
        ml_model_by_name_and_version = ml_model_client.get_manual_model(name="my_manual_model", version="my_manual_version")
        ```
        """
        assert id or (name and version), "`id` 또는 (`name`, `version`) 중 한 개 이상의 값이 반드시 전달되어야 합니다."

        ml_models = self.list_ml_models(id=id, name=name, version=version)
        if len(ml_models) == 0:
            raise MLSClientError(code=404, msg="ML모델이 없습니다.")
        elif len(ml_models) > 1:
            raise MLSClientError(code=409, msg="같은 이름의 모델이 여러개 존재합니다.")

        if ml_models[0].model_type != "manual":
            raise MLSClientError(code=400, msg="일반 모델이 아닙니다.")

        return ManualModel(**self._request(method="GET", url=f"{MLS_MODELS_API_URL}/{ml_models[0].id}").results)

    def update_manual_model(
        self,
        manual_model: ManualModel,
        name: str = None,
        version: str = None,
        description: str = None,
        creator: str = None,
        model_lib: str = None,
        model_data: str = None,
        model_meta: dict = None,
        features: str = None,
        table: str = None,
        components: List[Component] = None,
    ) -> ManualModel:
        """
        일반 모델 정보를 수정합니다.

        ## Args

        - model: (`sktmls.models.ManualModel`) 일반 모델 객체
        - name: (str) (optional) 수정할 일반 모델 이름
        - version: (str) (optional) 수정할 일반 모델 버전
        - description: (optional) (str) 수정할 일반 모델 설명
        - creator: (optional) (str) 수정할 일반 모델 계정명
        - model_lib: (optional) (str) 수정할 일반 모델 라이브러리
        - model_data: (optional) (str) 수정할 일반 모델 데이터
        - model_meta: (optional) (dict) 수정할 모델 레지스트리에 등록된 메타정보(model.json)
        - features: (optional) (str) 수정할 일반 모델에 사용된 피쳐
        - table: (optional) (str) 수정할 일반 모델 테이블
        - components: (optional) list(`sktmls.components.Component`) 수정할 일반 모델 컴포넌트 리스트

        ## Returns
        `sktmls.models.ManualModel`

        - id: (int) ML모델 고유 ID
        - name: (str) ML모델 이름
        - model_type: (str) ML모델 타입 (`automl` | `manual`)
        - version: (str) ML모델 버전
        - description: (str) ML모델 설명
        - creator: (str) ML모델 생성 계정명
        - status: (`sktmls.models.MLModelStatus`) ML모델 상태
        - model_meta: (dict) ML모델 메타정보
        - components: list(dict) ML모델 컴포넌트
        - table: (str) ML모델 테이블
        - model_lib: (str) ML모델 라이브러리
        - model_data: (str) ML모델 데이터
        - features: (str) ML모델에 사용된 피쳐
        - is_enabled: (bool) 활성상태 여부

        ## Example

        ```
        manual_model = ml_model_client.get_manual_model(name="my_manual_model", version="v1")
        manual_model = ml_model_client.update_manual_model(
            manual_model=manual_model,
            name="my_new_manual_model",
            description="updated manual model",
            model_data="/models/my_new_manual_model/v1/model.joblib",
        )
        ```
        """
        assert type(manual_model) == ManualModel

        data = {
            "name": manual_model.name,
            "version": manual_model.version,
            "model_type": "manual",
        }
        if manual_model.description is not None:
            data["description"] = manual_model.description
        if manual_model.creator is not None:
            data["creator"] = manual_model.creator
        if manual_model.model_lib is not None:
            data["model_lib"] = manual_model.model_lib
        if manual_model.model_data is not None:
            data["model_data"] = manual_model.model_data
        if manual_model.model_meta is not None:
            data["model_meta"] = manual_model.model_meta
        if manual_model.features is not None:
            data["features"] = manual_model.features
        if manual_model.table is not None:
            data["table"] = manual_model.table
        if manual_model.components is not None:
            data["components"] = [component.get("name") for component in manual_model.components]

        if name:
            data["name"] = name
        if version:
            data["version"] = version
        if description is not None:
            data["description"] = description
        if creator is not None:
            data["creator"] = creator
        if model_lib is not None:
            assert model_lib in MODEL_LIBS, "허용되지 않는 `model_lib`값입니다."
            data["model_lib"] = model_lib
        if model_data is not None:
            data["model_data"] = model_data
        if model_meta is not None:
            data["model_meta"] = model_meta
        if features is not None:
            data["features"] = features
        if table is not None:
            data["table"] = table
        if components is not None:
            for component in components:
                assert type(component) == Component, "`components`는 list(`sktmls.components.Component`) 형태여야 합니다."
            data["components"] = [component.name for component in components]

        updated_model_id = self._request(
            method="PUT", url=f"{MLS_MODELS_API_URL}/{manual_model.id}", data=data
        ).results.get("id")

        manual_model.reset(**self.get_manual_model(id=updated_model_id).get())
        return manual_model

    def delete_model(self, model: Union[AutoMLModel, ManualModel]) -> MLSResponse:
        """
        모델 삭제합니다.

        ## Args

        - model: (`sktmls.models.AutoMLModel` or `sktmls.models.ManualModel`) AutoML 혹은 일반 모델 객체

        ## Returns
        `sktmls.MLSResponse`

        ## Example

        ```
        ml_model_client.delete_model(model)
        ```
        """

        assert type(model) in [
            AutoMLModel,
            ManualModel,
        ], "`model`은 `sktmls.models.AutoMLModel` 혹은 `sktmls.models.ManualModel` 타입이어야 합니다."

        return self._request(method="DELETE", url=f"{MLS_MODELS_API_URL}/{model.id}")

    def update_manual_model_meta(
        self, manual_model: ManualModel, model_meta: dict, partial_update: bool = False,
    ) -> ManualModel:
        """
        일반 모델의 모델 메타 정보를 수정합니다.

        ## Args

        - model: (`sktmls.models.ManualModel`) 일반 모델 객체
        - model_meta: (dict) 수정할 모델 메타 정보
        - partial_update: (optional) (dict) 기존 모델 메타에 덮어씌울지(True) 기존 모델 메타를 교체할지(False) 여부 (기본값: `False`)

        ## Returns
        `sktmls.models.ManualModel`

        - id: (int) ML모델 고유 ID
        - name: (str) ML모델 이름
        - model_type: (str) ML모델 타입 (`automl` | `manual`)
        - version: (str) ML모델 버전
        - description: (str) ML모델 설명
        - creator: (str) ML모델 생성 계정명
        - status: (`sktmls.models.MLModelStatus`) ML모델 상태
        - model_meta: (dict) ML모델 메타정보
        - components: list(dict) ML모델 컴포넌트
        - table: (str) ML모델 테이블
        - model_lib: (str) ML모델 라이브러리
        - model_data: (str) ML모델 데이터
        - features: (str) ML모델에 사용된 피쳐
        - is_enabled: (bool) 활성상태 여부

        ## Example

        ```
        manual_model = ml_model_client.get_manual_model(name="my_manual_model", version="v1")
        manual_model = ml_model_client.update_manual_model_meta(
            manual_model=manual_model,
            model_meta={
                "model_lib": "xgboost",
                "model_lib_version": "1.2.0",
            },
            partial_update = True
        )
        manual_model_without_meta = ml_model_client.update_manual_model_meta(
            manual_model=manual_model,
            model_meta={}
        )

        ```
        """
        assert type(manual_model) == ManualModel

        if not partial_update:
            return self.update_manual_model(manual_model=manual_model, model_meta=model_meta)

        data = manual_model.model_meta
        data.update(model_meta)

        return self.update_manual_model(manual_model=manual_model, model_meta=data)

    def update_manual_model_components(self, manual_model: ManualModel, components: List[Component],) -> ManualModel:
        """
        일반 모델의 컴포넌트 정보를 수정합니다.

        ## Args

        - model: (`sktmls.models.ManualModel`) 일반 모델 객체
        - components: list(`sktmls.components.Component`) 수정할 컴포넌트 리스트

        ## Returns
        `sktmls.models.ManualModel`

        - id: (int) ML모델 고유 ID
        - name: (str) ML모델 이름
        - model_type: (str) ML모델 타입 (`automl` | `manual`)
        - version: (str) ML모델 버전
        - description: (str) ML모델 설명
        - creator: (str) ML모델 생성 계정명
        - status: (`sktmls.models.MLModelStatus`) ML모델 상태
        - model_meta: (dict) ML모델 메타정보
        - components: list(dict) ML모델 컴포넌트
        - table: (str) ML모델 테이블
        - model_lib: (str) ML모델 라이브러리
        - model_data: (str) ML모델 데이터
        - features: (str) ML모델에 사용된 피쳐
        - is_enabled: (bool) 활성상태 여부

        ## Example

        ```
        component = component_client.get_component(name="test_component")
        manual_model = ml_model_client.get_manual_model(name="manual_test_model", version="v1")

        updated_manual_model = ml_model_client.update_manual_model_components(
            manual_model=manual_model,
            components=[component],
        )
        no_component_manual_model = ml_model_client.update_manual_model_components(
            manual_model=manual_model,
            components=[],
        )

        ```
        """
        assert type(manual_model) == ManualModel
        for component in components:
            assert type(component) == Component, "`components`는 list(`sktmls.components.Component`) 형태여야 합니다."

        return self.update_manual_model(manual_model=manual_model, components=components)
