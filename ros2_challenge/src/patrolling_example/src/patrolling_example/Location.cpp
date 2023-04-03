// Copyright 2023 Óscar Martínez
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <string>
#include <future>

#include "patrolling_example/Location.hpp"

#include "behaviortree_cpp_v3/behavior_tree.h"
#include "geometry_msgs/msg/twist.hpp"
#include "rclcpp/rclcpp.hpp"

namespace patrolling_example
{

using namespace std::chrono_literals;

Location::Location(
  const std::string & xml_tag_name,
  const BT::NodeConfiguration & conf)
: BT::ActionNodeBase(xml_tag_name, conf)
{
  config().blackboard->get("node", node_);

  auto qos = rclcpp::QoS(rclcpp::QoSInitialization(RMW_QOS_POLICY_HISTORY_KEEP_LAST, 5));
  qos.reliability(RMW_QOS_POLICY_RELIABILITY_RELIABLE);
}

void
Location::halt()
{
  std::cout << "Patrol halt" << std::endl;
}

BT::NodeStatus
Location::tick()
{
  RCLCPP_INFO(node_->get_logger(), "I have arrived to the location");
  return BT::NodeStatus::SUCCESS;
}

}  // namespace patrolling_ros2d2

#include "behaviortree_cpp_v3/bt_factory.h"
BT_REGISTER_NODES(factory)
{
  factory.registerNodeType<patrolling_example::Location>("Location");
}
