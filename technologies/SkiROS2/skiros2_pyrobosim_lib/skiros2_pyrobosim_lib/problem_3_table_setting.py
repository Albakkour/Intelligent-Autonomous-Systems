from skiros2_skill.core.skill import (
    SkillDescription,
    SkillBase,
    SerialStar,
    RetryOnFail,
)
from skiros2_common.core.params import ParamTypes
from skiros2_common.core.world_element import Element
from .pyrobosim_compound_skills import (
    Navigate,
    Pick,
    Place,
    OpenOpenableLocation,
    CloseOpenableLocation,
)

#################################################################################
# Descriptions
#################################################################################


class Problem3(SkillDescription):
    def createDescription(self):
        # =======Params=========
        self.addParam("Table", Element("skiros:Table"), ParamTypes.Required)
        self.addParam("Bread", Element("skiros:Bread"), ParamTypes.Required)
        self.addParam("Butter", Element("skiros:Butter"), ParamTypes.Required)
        self.addParam("Fridge", Element("skiros:Fridge"), ParamTypes.Inferred)
        self.addParam("Pantry", Element("skiros:Pantry"), ParamTypes.Inferred)
        self.addParam("Gripper", Element("rparts:GripperEffector"), ParamTypes.Inferred)

        # =======PreConditions=========
        self.addPreCondition(
            self.getRelationCond(
                "RobotHasAGripper", "skiros:hasA", "Robot", "Gripper", True
            )
        )
        self.addPreCondition(
            self.getPropCond(
                "EmptyHanded", "skiros:ContainerState", "Gripper", "=", "Empty", True
            )
        )
        self.addPreCondition(
            self.getRelationCond(
                "FridgeContainsButter", "skiros:contain", "Fridge", "Butter", True
            )
        )
        self.addPreCondition(
            self.getRelationCond(
                "PantryContainsBread", "skiros:contain", "Pantry", "Bread", True
            )
        )

        # =======PostConditions=========
        self.addPostCondition(
            self.getPropCond(
                "EmptyHanded", "skiros:ContainerState", "Gripper", "=", "Empty", True
            )
        )
        self.addPostCondition(
            self.getRelationCond(
                "TableContainsBread", "skiros:contain", "Table", "Bread", True
            )
        )
        self.addPostCondition(
            self.getRelationCond(
                "TableContainsButter", "skiros:contain", "Table", "Butter", True
            )
        )
        self.addPostCondition(
            self.getPropCond("FridgeClosed", "skiros:Open", "Fridge", "=", False, True)
        )
        self.addPostCondition(
            self.getPropCond("PantryClosed", "skiros:Open", "Pantry", "=", False, True)
        )


#################################################################################
# Implementations
#################################################################################


class navigate_with_retry(SkillBase):
    """ """

    def createDescription(self):
        self.setDescription(Navigate(), "Navigate to Location with Retry")

    def expand(self, skill):
        skill(
            # 3.1: retry the (fallible) pyrobosim action up to 10 times
            self.skill(RetryOnFail(10))(
                self.skill("NavigateExecution", ""),
            ),
            self.skill(
                "WmSetRelation",
                "wm_set_relation",
                remap={"Dst": "TargetLocation", "OldDstToRemove": "StartLocation"},
                specify={
                    "Src": self.params["Robot"].value,
                    "Relation": "skiros:at",
                    "RelationState": True,
                },
            ),
        )


class pick_with_retry(SkillBase):
    def createDescription(self):
        self.setDescription(Pick(), "Pick Part with Retry")

    def expand(self, skill):
        skill(
            # 3.1: retry the pick up to 10 times
            self.skill(RetryOnFail(10))(
                self.skill("PickExecution", ""),
            ),
            self.skill(
                "WmMoveObject",
                "wm_move_object",
                remap={"StartLocation": "Container", "TargetLocation": "Gripper"},
            ),
        )


class place_with_retry(SkillBase):
    def createDescription(self):
        self.setDescription(Place(), "Place Part with Retry")

    def expand(self, skill):
        skill(
            # 3.1: retry the place up to 10 times
            self.skill(RetryOnFail(10))(
                self.skill("PlaceExecution", ""),
            ),
            self.skill(
                "WmMoveObject",
                "wm_move_object",
                remap={"StartLocation": "Gripper", "TargetLocation": "PlacingLocation"},
            ),
        )


class open_openablelocation_with_retry(SkillBase):
    def createDescription(self):
        self.setDescription(OpenOpenableLocation(), "Open Location with Retry")

    def expand(self, skill):
        skill(
            # 3.1: retry opening up to 10 times
            self.skill(RetryOnFail(10))(
                self.skill("OpenExecution", ""),
            ),
            self.skill(
                "WmSetProperties",
                "",
                remap={"Src": "OpenableLocation"},
                specify={"Properties": {"skiros:Open": True}},
            ),
        )


class close_openablelocation_with_retry(SkillBase):
    def createDescription(self):
        self.setDescription(
            CloseOpenableLocation(), "Close OpenableLocation with Retry"
        )

    def expand(self, skill):
        skill(
            # 3.1: retry closing up to 10 times
            self.skill(RetryOnFail(10))(
                self.skill("CloseExecution", ""),
            ),
            self.skill(
                "WmSetProperties",
                "",
                remap={"Src": "OpenableLocation"},
                specify={"Properties": {"skiros:Open": False}},
            ),
        )


class problem_3(SkillBase):
    """ """

    def createDescription(self):
        self.setAvailableForPlanning(False)
        self.setDescription(Problem3(), "Problem 3 - Setting the Table")

    def expand(self, skill):
        skill.setProcessor(SerialStar())
        skill(
            # 3.2: Fetch the bread (Problem1 opens the pantry, picks the bread and puts it on the table)
            self.skill(SerialStar())(
                self.skill(
                    "Problem1",
                    "problem_1",
                    remap={"ObjectTargetLocation": "Table", "Object": "Bread"},
                ),
                # Now close the pantry. The robot is at the Table after Problem1,
                # so StartLocation = Table.
                self.skill(
                    "Navigate",
                    "",
                    remap={"TargetLocation": "Pantry", "StartLocation": "Table"},
                ),
                self.skill("CloseLocation", "", remap={"Location": "Pantry"}),
                # Unset some blackboard parameters to avoid conflicts. Nothing to do here.
                self.skill("BbUnsetParam", "", remap={"Parameter": "StartLocation"}),
                self.skill(
                    "BbUnsetParam", "", remap={"Parameter": "ObjectStartLocation"}
                ),
                self.skill("BbUnsetParam", "", remap={"Parameter": "Container"}),
            ),
            # 3.3: Fetch the butter and close the fridge (same pattern as for the bread)
            self.skill(SerialStar())(
                self.skill(
                    "Problem1",
                    "problem_1",
                    remap={"ObjectTargetLocation": "Table", "Object": "Butter"},
                ),
                self.skill(
                    "Navigate",
                    "",
                    remap={"TargetLocation": "Fridge", "StartLocation": "Table"},
                ),
                self.skill("CloseLocation", "", remap={"Location": "Fridge"}),
                # Same clean-up as above, so this skill can be reused (e.g. in Problem 4)
                self.skill("BbUnsetParam", "", remap={"Parameter": "StartLocation"}),
                self.skill(
                    "BbUnsetParam", "", remap={"Parameter": "ObjectStartLocation"}
                ),
                self.skill("BbUnsetParam", "", remap={"Parameter": "Container"}),
            ),
        )
