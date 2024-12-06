import pytest
import model


# Test model.TrackedAsset functionality
def test_tracked_asset_initialization():
    asset = model.TrackedAsset([1, 2, 3, 4], 1, "hub_set_1")
    assert asset.current_version == 1
    assert asset.hub_set_name == "hub_set_1"
    assert asset.available_versions == (4, 3, 2, 1)


def test_tracked_asset_set_version():
    asset = model.TrackedAsset([1, 2, 3, 4], 1, "hub_set_1")
    asset.set_version(2)
    assert asset.new_version == 2


def test_tracked_asset_set_invalid_version():
    asset = model.TrackedAsset([1, 2, 3, 4], 1, "hub_set_1")
    with pytest.raises(ValueError):
        asset.set_version(5)  # Invalid version


def test_tracked_asset_to_command_create():
    asset = model.TrackedAsset([1, 2, 3, 4])
    asset.set_version(1)
    assert asset.to_command() == "create 1"


def test_tracked_asset_to_command_update():
    asset = model.TrackedAsset([1, 2, 3, 4], 1, "hub_set_1")
    asset.set_version(2)
    assert asset.to_command() == "update hub_set_1 from 1 to 2"


def test_tracked_asset_to_command_remove():
    asset = model.TrackedAsset([1, 2, 3, 4], 1, "hub_set_1")
    asset.set_version(None)
    assert asset.to_command() == "remove hub_set_1"


def test_tracked_asset_to_command_still():
    asset = model.TrackedAsset([1, 2, 3, 4], 1, "hub_set_1")
    asset.set_version(1)  # Same version
    assert asset.to_command() == "still"


# Test model.AssetPackage functionality
def test_asset_package_initialization():
    assets = {
        "root_asset": model.TrackedAsset([1, 2, 3], 1, "hub_root"),
        "child_asset": model.TrackedAsset([1, 2, 3], 1, "hub_child"),
    }
    package = model.AssetPackage("root_asset", assets)
    assert package.root_asset_key == "root_asset"
    assert package.root_asset.current_version == 1
    assert "child_asset" in package.child_assets


def test_asset_package_to_command_with_root_update():
    assets = {
        "root_asset": model.TrackedAsset([1, 2, 3], 1, "hub_root"),
        "child_asset": model.TrackedAsset([1, 2, 3], 1, "hub_child"),
    }
    package = model.AssetPackage("root_asset", assets)
    package.root_asset.set_version(2)
    commands = package.to_command()
    assert commands == ["hub_root", "update hub_root from 1 to 2"]


def test_asset_package_to_command_with_children():
    assets = {
        "root_asset": model.TrackedAsset([1, 2, 3], 1, "hub_root"),
        "child_asset": model.TrackedAsset([1, 2, 3], 1, "hub_child"),
    }
    package = model.AssetPackage("root_asset", assets)
    package.child_assets["child_asset"].set_version(2)
    commands = package.to_command()
    assert commands == ["hub_root", ("child_asset", "update hub_child from 1 to 2")]


def test_asset_package_with_no_changes():
    assets = {
        "root_asset": model.TrackedAsset([1, 2, 3], 1, "hub_root"),
        "child_asset": model.TrackedAsset([1, 2, 3], 1, "hub_child"),
    }
    package = model.AssetPackage("root_asset", assets)
    commands = package.to_command()
    assert commands == ["hub_root", ("child_asset", "still")]
