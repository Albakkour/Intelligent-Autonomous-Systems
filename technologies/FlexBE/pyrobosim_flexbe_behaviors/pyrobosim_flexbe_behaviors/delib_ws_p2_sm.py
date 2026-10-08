#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2024 David Conner
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#  1. Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.

#  2. Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
#  3. Neither the name of the copyright holder nor the names of its
#     contributors may be used to endorse or promote products derived from
#     this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS”
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
# TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

"""
Define TransportItems.

Generic behavior for transporting two configurable items from their source
location to a destination.

Created on Sat Aug 31 2024
@author: David Conner & Mohamed Albakkour
"""


from flexbe_core import Autonomy
from flexbe_core import Behavior
from flexbe_core import ConcurrencyContainer
from flexbe_core import Logger
from flexbe_core import OperatableStateMachine
from flexbe_core import PriorityContainer
from flexbe_core import initialize_flexbe_core
from flexbe_states.check_condition_state import CheckConditionState
from flexbe_states.operator_decision_state import OperatorDecisionState
from pyrobosim_flexbe_behaviors.navigateandact_sm import NavigateAndActSM
from pyrobosim_flexbe_behaviors.processwaste_sm import ProcessWasteSM
from pyrobosim_flexbe_behaviors.verifyaccess_sm import VerifyAccessSM
from pyrobosim_flexbe_behaviors.verifywaste_sm import VerifyWasteSM

# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]


# [/MANUAL_IMPORT]


class TransportItemsSM(Behavior):
    """
    Define TransportItems.

    Generic behavior for transporting two configurable items from their source
    location to a destination.
    """

    def __init__(self, node):
        super().__init__()
        self.name = 'TransportItems'

        # parameters of this behavior
        self.add_parameter('tasks', '[waste0,waste1]')
        self.add_parameter('access_location', '')
        self.add_parameter('destination_location', '')
        self.add_parameter('item0', '')
        self.add_parameter('source0', '')
        self.add_parameter('item1', '')
        self.add_parameter('source1', '')
        self.add_parameter('use_access', False)
        self.add_parameter('close_destination', False)

        # Initialize ROS node information
        initialize_flexbe_core(node)

        # references to used behaviors
        self.add_behavior(NavigateAndActSM, 'CloseDestination', node)
        self.add_behavior(VerifyAccessSM, 'VerifyAccess', node)
        self.add_behavior(VerifyWasteSM, 'VerifyWaste', node)
        self.add_behavior(ProcessWasteSM, 'WasteLoop/ProcessWaste0', node)
        self.add_behavior(ProcessWasteSM, 'WasteLoop/ProcessWaste1', node)

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]


        # [/MANUAL_INIT]

        # Behavior comments:

    def create(self):
        """Create state machine."""
        # Root state machine
        # x:172 y:332, x:1255 y:289
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
        _state_machine.userdata.tasks = self.tasks
        _state_machine.userdata.access_goal = self.access_location
        _state_machine.userdata.destination_goal = self.destination_location
        _state_machine.userdata.item0 = self.item0
        _state_machine.userdata.source0 = self.source0
        _state_machine.userdata.item1 = self.item1
        _state_machine.userdata.source1 = self.source1
        _state_machine.userdata.use_access = self.use_access
        _state_machine.userdata.close_destination = self.close_destination

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]


        # [/MANUAL_CREATE]

        # x:755 y:528, x:1075 y:86
        _sm_wasteloop_0 = OperatableStateMachine(outcomes=['finished', 'failed'],
                                                 input_keys=['tasks'])

        with _sm_wasteloop_0:
            # x:283 y:121
            OperatableStateMachine.add('CheckWaste0',
                                       CheckConditionState(predicate=lambda x: self.item0 in x),
                                       transitions={'true': 'ProcessWaste0'  # 564 102 -1 -1 -1 -1
                                                    , 'false': 'CheckWaste1'  # 487 220 -1 -1 -1 -1
                                                    },
                                       autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                       remapping={'input_value': 'tasks'})

            # x:461 y:277
            OperatableStateMachine.add('CheckWaste1',
                                       CheckConditionState(predicate=lambda x: self.item1 in x),
                                       transitions={'true': 'ProcessWaste1'  # 689 297 -1 -1 -1 -1
                                                    , 'false': 'finished'  # 646 432 -1 -1 -1 -1
                                                    },
                                       autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                       remapping={'input_value': 'tasks'})

            # x:640 y:98
            OperatableStateMachine.add('ProcessWaste0',
                                       self.use_behavior(ProcessWasteSM, 'WasteLoop/ProcessWaste0',
                                                         parameters={'source_location': self.source0,
                                                                     'destination_location': self.destination_location}),
                                       transitions={'finished': 'CheckWaste1'  # 556 205 -1 -1 -1 -1
                                                    , 'failed': 'ProcessWaste0'  # 691 45 -1 -1 -1 -1
                                                    },
                                       autonomy={'finished': Autonomy.Inherit,
                                                 'failed': Autonomy.Inherit})

            # x:725 y:276
            OperatableStateMachine.add('ProcessWaste1',
                                       self.use_behavior(ProcessWasteSM, 'WasteLoop/ProcessWaste1',
                                                         parameters={'source_location': self.source1,
                                                                     'destination_location': self.destination_location}),
                                       transitions={'finished': 'finished'  # 794 432 -1 -1 -1 -1
                                                    , 'failed': 'ProcessWaste1'  # 836 223 -1 -1 -1 -1
                                                    },
                                       autonomy={'finished': Autonomy.Inherit,
                                                 'failed': Autonomy.Inherit})

        with _state_machine:
            # x:168 y:100
            OperatableStateMachine.add('OpDecision',
                                       OperatorDecisionState(outcomes=['go', 'quit'],
                                                             hint="Go to table",
                                                             suggestion='go'),
                                       transitions={'go': 'ChechAccess'  # 417 10 -1 -1 -1 -1
                                                    , 'quit': 'finished'  # 170 237 207 153 -1 -1
                                                    },
                                       autonomy={'go': Autonomy.High, 'quit': Autonomy.Full})

            # x:458 y:22
            OperatableStateMachine.add('ChechAccess',
                                       CheckConditionState(predicate=lambda x: x),
                                       transitions={'true': 'VerifyAccess'  # 672 15 -1 -1 -1 -1
                                                    , 'false': 'WasteLoop'  # 574 246 -1 -1 -1 -1
                                                    },
                                       autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                       remapping={'input_value': 'use_access'})

            # x:12 y:457
            OperatableStateMachine.add('CheckCloseDestination',
                                       CheckConditionState(predicate=lambda x: x),
                                       transitions={'true': 'CloseDestination'  # 227 453 -1 -1 -1 -1
                                                    , 'false': 'finished'  # 118 399 -1 -1 -1 -1
                                                    },
                                       autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                       remapping={'input_value': 'close_destination'})

            # x:249 y:396
            OperatableStateMachine.add('CloseDestination',
                                       self.use_behavior(NavigateAndActSM, 'CloseDestination',
                                                         parameters={'navigation_goal': self.destination_location,
                                                                     'action_type': "close"}),
                                       transitions={'finished': 'finished'  # 226 374 -1 -1 -1 -1
                                                    , 'failed': 'CheckCloseDestination'  # 170 412 -1 -1 -1 -1
                                                    },
                                       autonomy={'finished': Autonomy.Inherit,
                                                 'failed': Autonomy.Inherit})

            # x:762 y:116
            OperatableStateMachine.add('VerifyAccess',
                                       self.use_behavior(VerifyAccessSM, 'VerifyAccess',
                                                         parameters={'access_location': self.access_location,
                                                                     'target_location': self.destination_location}),
                                       transitions={'finished': 'WasteLoop'  # 502 275 -1 -1 -1 -1
                                                    , 'failed': 'VerifyAccess'  # 1001 249 -1 -1 -1 -1
                                                    },
                                       autonomy={'finished': Autonomy.Inherit,
                                                 'failed': Autonomy.Inherit})

            # x:167 y:632
            OperatableStateMachine.add('VerifyWaste',
                                       self.use_behavior(VerifyWasteSM, 'VerifyWaste',
                                                         parameters={'item0': self.item0,
                                                                     'item1': self.item1,
                                                                     'destination_location': self.destination_location}),
                                       transitions={'finished': 'CheckCloseDestination'  # 177 585 -1 -1 -1 -1
                                                    , 'failed': 'WasteLoop'  # 467 554 -1 -1 -1 -1
                                                    },
                                       autonomy={'finished': Autonomy.Inherit,
                                                 'failed': Autonomy.Inherit})

            # x:616 y:397
            OperatableStateMachine.add('WasteLoop',
                                       _sm_wasteloop_0,
                                       transitions={'finished': 'VerifyWaste'  # 449 557 -1 -1 -1 -1
                                                    , 'failed': 'failed'  # 1041 368 -1 -1 -1 -1
                                                    },
                                       autonomy={'finished': Autonomy.Inherit,
                                                 'failed': Autonomy.Inherit},
                                       remapping={'tasks': 'tasks'})

        return _state_machine

    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]


    # [/MANUAL_FUNC]
