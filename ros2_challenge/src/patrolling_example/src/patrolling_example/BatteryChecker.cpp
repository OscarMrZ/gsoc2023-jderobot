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
#include <iostream>
#include <algorithm>

#include "patrolling_example/BatteryChecker.hpp"

#include "behaviortree_cpp_v3/behavior_tree.h"
#include "geometry_msgs/msg/twist.hpp"
#include "rclcpp/rclcpp.hpp"

namespace patrolling_example
{

using namespace std::chrono_literals;
using namespace std::placeholders;

BatteryChecker::BatteryChecker(
  const std::string & xml_tag_name,
  const BT::NodeConfiguration & conf)
: BT::ConditionNode(xml_tag_name, conf)
{
  config().blackboard->get("node", node_);

  vel_sub_ = node_->create_subscription<geometry_msgs::msg::Twist>(
    "/output_vel", 100, std::bind(&BatteryChecker::vel_callback, this, _1));

  last_reading_time_ = node_->now();
  last_battery_msg_ = node_->now();
}

void
BatteryChecker::vel_callback(const geometry_msgs::msg::Twist::SharedPtr msg)
{
  last_twist_ = *msg;
}

void
BatteryChecker::update_battery()
{
  float battery_level;
  if (!config().blackboard->get("battery_level", battery_level)) {
    battery_level = 100.0f;
  }

  float dt = (node_->now() - last_reading_time_).seconds();
  last_reading_time_ = node_->now();

  float vel = sqrt(
    last_twist_.linear.x * last_twist_.linear.x +
    last_twist_.angular.z * last_twist_.angular.z);
  battery_level = std::max(0.0f, battery_level - (vel * dt * DECAY_LEVEL) - EPSILON * dt);

  config().blackboard->set("battery_level", battery_level);
}

BT::NodeStatus
BatteryChecker::tick()
{
  update_battery();

  float battery_level;
  config().blackboard->get("battery_level", battery_level);

  // Only print the battery level every 10 seconds
  if (node_->now() - last_battery_msg_ > 10s) {
    RCLCPP_INFO(node_->get_logger(), "Battery level: %f", battery_level);
    last_battery_msg_ = node_->now();
  }

  if (battery_level < MIN_LEVEL) {
    RCLCPP_INFO(node_->get_logger(), "Battery level low, returning to base");
    return BT::NodeStatus::FAILURE;
  } else {
    return BT::NodeStatus::SUCCESS;
  }
}

}  // namespace patrolling_example

#include "behaviortree_cpp_v3/bt_factory.h"
BT_REGISTER_NODES(factory)
{
  factory.registerNodeType<patrolling_example::BatteryChecker>("BatteryChecker");
}
