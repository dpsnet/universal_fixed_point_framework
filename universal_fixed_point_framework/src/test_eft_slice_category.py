import numpy as np
import pytest
from eft_slice_category import (
    EFTTheory, RGFlow, EFTSliceCategory,
    RGFlowFunctor, SpectralSilenceFunctor,
    AdjunctionRelation
)


class TestEFTTheory:
    def test_creation(self):
        theory = EFTTheory(
            name="QCD",
            energy_scale=100,
            degrees_of_freedom=3,
            coupling_constants={"g": 0.1},
            spectrum=np.array([1.0, 2.0, 3.0])
        )
        assert theory.name == "QCD"
        assert theory.energy_scale == 100
        assert theory.degrees_of_freedom == 3

    def test_equality(self):
        t1 = EFTTheory(
            name="QCD",
            energy_scale=100,
            degrees_of_freedom=3,
            coupling_constants={"g": 0.1},
            spectrum=np.array([1.0, 2.0, 3.0])
        )
        t2 = EFTTheory(
            name="QCD",
            energy_scale=100,
            degrees_of_freedom=3,
            coupling_constants={"g": 0.1},
            spectrum=np.array([1.0, 2.0, 3.0])
        )
        assert t1.name == t2.name
        assert t1.energy_scale == t2.energy_scale


class TestRGFlow:
    def test_creation(self):
        source = EFTTheory(
            name="UV",
            energy_scale=1000,
            degrees_of_freedom=3,
            coupling_constants={"g": 0.1},
            spectrum=np.array([1.0, 2.0, 3.0])
        )
        target = EFTTheory(
            name="IR",
            energy_scale=100,
            degrees_of_freedom=3,
            coupling_constants={"g": 0.5},
            spectrum=np.array([1.0, 2.0, 3.0])
        )
        flow = RGFlow(
            source=source,
            target=target,
            name="RG1",
            scale_factor=0.1,
            beta_functions={"g": lambda g: -g**3}
        )
        assert flow.source == source
        assert flow.target == target

    def test_flow_properties(self):
        t1 = EFTTheory(
            name="T1",
            energy_scale=1000,
            degrees_of_freedom=3,
            coupling_constants={"g": 0.1},
            spectrum=np.array([1.0, 2.0, 3.0])
        )
        t2 = EFTTheory(
            name="T2",
            energy_scale=100,
            degrees_of_freedom=3,
            coupling_constants={"g": 0.5},
            spectrum=np.array([1.0, 2.0, 3.0])
        )
        f1 = RGFlow(
            source=t1,
            target=t2,
            name="F1",
            scale_factor=0.1,
            beta_functions={"g": lambda g: -g**3}
        )
        assert f1.source == t1
        assert f1.target == t2
        assert f1.scale_factor == 0.1


class TestEFTSliceCategory:
    def test_creation(self):
        lambda_theory = EFTTheory(
            name="Lambda",
            energy_scale=100,
            degrees_of_freedom=3,
            coupling_constants={"g": 0.5},
            spectrum=np.array([1.0, 2.0, 3.0])
        )
        category = EFTSliceCategory(lambda_theory)
        assert "EFT" in category.name
        assert "Lambda" in category.name
        assert category.lambda_theory == lambda_theory

    def test_add_slice_object(self):
        lambda_theory = EFTTheory(
            name="Lambda",
            energy_scale=100,
            degrees_of_freedom=3,
            coupling_constants={"g": 0.5},
            spectrum=np.array([1.0, 2.0, 3.0])
        )
        category = EFTSliceCategory(lambda_theory)
        t1 = EFTTheory(
            name="UV",
            energy_scale=1000,
            degrees_of_freedom=3,
            coupling_constants={"g": 0.1},
            spectrum=np.array([1.0, 2.0, 3.0])
        )
        pi_t1 = RGFlow(
            source=t1,
            target=lambda_theory,
            name="Pi_UV",
            scale_factor=0.1,
            beta_functions={"g": lambda g: -g**3}
        )
        category.add_slice_object(t1, pi_t1)
        assert "UV" in category.slice_objects

    def test_add_slice_morphism(self):
        lambda_theory = EFTTheory(
            name="Lambda",
            energy_scale=100,
            degrees_of_freedom=3,
            coupling_constants={"g": 0.5},
            spectrum=np.array([1.0, 2.0, 3.0])
        )
        category = EFTSliceCategory(lambda_theory)
        t1 = EFTTheory(
            name="UV",
            energy_scale=1000,
            degrees_of_freedom=3,
            coupling_constants={"g": 0.1},
            spectrum=np.array([1.0, 2.0, 3.0])
        )
        t2 = EFTTheory(
            name="IR",
            energy_scale=500,
            degrees_of_freedom=3,
            coupling_constants={"g": 0.3},
            spectrum=np.array([1.0, 2.0, 3.0])
        )
        pi_t1 = RGFlow(
            source=t1,
            target=lambda_theory,
            name="Pi_UV",
            scale_factor=0.1,
            beta_functions={"g": lambda g: -g**3}
        )
        pi_t2 = RGFlow(
            source=t2,
            target=lambda_theory,
            name="Pi_IR",
            scale_factor=0.5,
            beta_functions={"g": lambda g: -g**3}
        )
        f = RGFlow(
            source=t1,
            target=t2,
            name="F12",
            scale_factor=0.5,
            beta_functions={"g": lambda g: -g**3}
        )
        slice_obj1 = category.add_slice_object(t1, pi_t1)
        slice_obj2 = category.add_slice_object(t2, pi_t2)
        result = category.add_slice_morphism(slice_obj1, slice_obj2, f)
        assert result is not None
        assert result.source == slice_obj1
        assert result.target == slice_obj2


class TestRGFlowFunctor:
    def test_creation(self):
        lambda_theory = EFTTheory(
            name="Lambda",
            energy_scale=100,
            degrees_of_freedom=3,
            coupling_constants={"g": 0.5},
            spectrum=np.array([1.0, 2.0, 3.0])
        )
        target_category = EFTSliceCategory(lambda_theory)
        functor = RGFlowFunctor(target_category)
        assert functor.target_category == target_category

    def test_object_map(self):
        lambda_theory = EFTTheory(
            name="Lambda",
            energy_scale=100,
            degrees_of_freedom=3,
            coupling_constants={"g": 0.5},
            spectrum=np.array([1.0, 2.0, 3.0])
        )
        target_category = EFTSliceCategory(lambda_theory)
        functor = RGFlowFunctor(target_category)
        t1 = EFTTheory(
            name="QCD",
            energy_scale=1000,
            degrees_of_freedom=3,
            coupling_constants={"g": 0.1},
            spectrum=np.array([1.0, 2.0, 3.0])
        )
        result = functor.object_map(t1)
        assert result.theory == t1
        assert result.projection.target == lambda_theory


class TestSpectralSilenceFunctor:
    def test_creation(self):
        functor = SpectralSilenceFunctor()
        assert functor is not None

    def test_object_map(self):
        lambda_theory = EFTTheory(
            name="Lambda",
            energy_scale=100,
            degrees_of_freedom=3,
            coupling_constants={"g": 0.5},
            spectrum=np.array([1.0, 2.0, 3.0])
        )
        category = EFTSliceCategory(lambda_theory)
        t1 = EFTTheory(
            name="QCD",
            energy_scale=1000,
            degrees_of_freedom=3,
            coupling_constants={"g": 0.1},
            spectrum=np.array([1.0, 2.0, 3.0])
        )
        pi_t1 = RGFlow(
            source=t1,
            target=lambda_theory,
            name="Pi_QCD",
            scale_factor=0.1,
            beta_functions={"g": lambda g: -g**3}
        )
        category.add_slice_object(t1, pi_t1)
        functor = SpectralSilenceFunctor()
        slice_obj = category.slice_objects["QCD"]
        result = functor.object_map(slice_obj)
        assert result is not None


class TestAdjunction:
    def test_adjunction_triangle(self):
        lambda_theory = EFTTheory(
            name="Lambda",
            energy_scale=100,
            degrees_of_freedom=3,
            coupling_constants={"g": 0.5},
            spectrum=np.array([1.0, 2.0, 3.0])
        )
        category = EFTSliceCategory(lambda_theory)
        t1 = EFTTheory(
            name="QCD",
            energy_scale=1000,
            degrees_of_freedom=3,
            coupling_constants={"g": 0.1},
            spectrum=np.array([1.0, 2.0, 3.0])
        )
        pi_t1 = RGFlow(
            source=t1,
            target=lambda_theory,
            name="Pi_QCD",
            scale_factor=0.1,
            beta_functions={"g": lambda g: -g**3}
        )
        category.add_slice_object(t1, pi_t1)
        W = RGFlowFunctor(category)
        S = SpectralSilenceFunctor()
        adj = AdjunctionRelation(W, S)
        result = adj.verify_triangle_identities()
        assert result["first_triangle"] is True
        assert result["second_triangle"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])