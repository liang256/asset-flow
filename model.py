class TrackedAsset:
    """
    Represents an individual asset in the pipeline, tracking its version and hub set association.

    Attributes:
        available_versions (tuple): Sorted tuple of available asset version URIs.
        current_version (str): The current version URI of the asset. Should not be modified.
        hub_set_name (str): The associated hub set name. Should not be modified.
        new_version (str): The target version URI for the asset.
    """

    def __init__(self, available_versions, current_version=None, hub_set_name=None):
        is_in_scene = current_version is not None and hub_set_name is not None
        is_new = current_version is None and hub_set_name is None
        if not is_in_scene and not is_new:
            raise ValueError(
                'Both "current_version" and "hub_set_name" must be provided, or both must be None'
            )

        self.available_versions = tuple(sorted(available_versions, reverse=True))
        self.current_version = current_version  # should not be modified
        self.hub_set_name = hub_set_name  # should not be modified
        self.new_version = current_version

    def __repr__(self):
        return f"TrackedAsset({self.current_version}->{self.new_version}, HubSet: {self.hub_set_name})"
    
    def __eq__(self, value):
        return (
            self.current_version == value.current_version
            and self.hub_set_name == value.hub_set_name
            and self.new_version == value.new_version
            and self.available_versions == value.available_versions
        )

    def set_version(self, new_version):
        """
        Sets the target version of the asset.

        Args:
            new_version (str | None): The new version to set.

        Raises:
            ValueError: If the version is not in the list of available versions.
        """
        if new_version is None:
            self.new_version = None
            return
        if new_version not in self.available_versions:
            raise ValueError(
                f"{new_version} is not in available versions: {self.available_versions}"
            )
        self.new_version = new_version

    def get_version(self):
        """
        Gets the target version of the asset.

        Returns:
            str: The target version URI.
        """
        return self.new_version

    def get_hub_set(self):
        """
        Gets the hub set name associated with the asset.

        Returns:
            str: The hub set name.
        """
        return self.hub_set_name

    def to_command(self):
        """
        Generates a command representing the desired operation for the asset.

        Returns:
            str: The command string.
        """
        if self.current_version == self.new_version:
            return "still"
        if self.current_version is None and self.hub_set_name is None:
            return f"create {self.new_version}"
        if self.new_version is None:
            return f"remove {self.hub_set_name}"
        return f"update {self.hub_set_name} from {self.current_version} to {self.new_version}"


class AssetPackage(dict):
    """
    Represents a package of assets, including a root asset and its associated child assets.

    Attributes:
        root_asset_key (str): The key identifying the root asset in the package.
    """

    def __init__(self, root_asset_key, assets):
        """
        Initializes an asset package.

        Args:
            root_asset_key (str): The key identifying the root asset.
            assets (dict): Dictionary of assets in the package.
        """
        super().__init__(assets)
        self.root_asset_key = root_asset_key

    @property
    def root_asset(self):
        """
        Gets the root asset of the package.

        Returns:
            TrackedAsset: The root asset.
        """
        return self[self.root_asset_key]

    @property
    def child_assets(self):
        """
        Gets the child assets of the package.

        Returns:
            dict: A dictionary of child assets.
        """
        return {key: value for key, value in self.items() if key != self.root_asset_key}

    def to_command(self):
        """
        Generates a list of commands for the package's assets.

        Returns:
            list: A list of commands.
        """
        commands = [self.root_asset.get_hub_set()]
        root_command = self.root_asset.to_command()
        if root_command != "still":
            commands.append(root_command)
            return commands

        for asset_type, child_asset in self.child_assets.items():
            child_cmd = child_asset.to_command()
            if child_cmd != "still":
                commands.append((asset_type, child_cmd))
        return commands if len(commands) > 1 else []
    
    def __repr__(self):
        return f"AssetPackage({self.root_asset_key}, {dict(self)})"


def generate_commands(packages):
    """
    Generates commands for a list of asset packages.

    Args:
        packages (list): List of AssetPackage objects.

    Returns:
        list: A list of commands for all packages.
    """
    return [pkg.to_command() for pkg in packages]


if __name__ == "__main__":
    asset = TrackedAsset([1, 2, 3, 4], 1, "hub_set_1")
    asset.set_version(2)
    print(asset.to_command())

    data = [
        AssetPackage(
            "camera_asset",
            assets={
                "camera_asset": TrackedAsset(["v1"], "v1", "hub_camera"),
                "camera_rig": TrackedAsset(["rig_v1", "rig_v2"]),
                "animation_curves": TrackedAsset(["anim_v1"]),
            },
        ),
        AssetPackage(
            "character_asset",
            assets={
                "character_asset": TrackedAsset(["v1", "v2", "v3"]),
                "rig_puppet": TrackedAsset(["rig_v1"]),
            },
        ),
    ]

    data[0]["camera_asset"].set_version("v1")
    data[1]["character_asset"].set_version("v3")

    print(generate_commands(data))
