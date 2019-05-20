# Snake_Project
Self learning snake robot project for 2nd year engineering school

The aim of the project was to build a snake robot from servo-motors and pilot it from a computer.

When that was done, we artificially "broke" one of them an went throught a genetic algorithm process to find the best solution in order to limp.

The 3 main part of the project are 

## 1] The Sevomotor dynamixel-AX12 command
To go throught the motor command, you'll need to install the [pydynamixel library](./servo_controlling/libs/pydynamixel/) see [Readme](Snake_Project/servo_controlling/libs/pydynamixel/README.md) for more informations.

You can then try to make them work with our [programs](./servo_controlling/program/).

## 2] The detection of the snake in space through image Processing

Image processing is at the center of our project as we need to find the snake in space and evaluate it's performance.

We choosed to use *pygame* as our image processing library as it was at the same time taking the pictures and processing them.
You may find more about image processing in [ImageProcessing](./ImageProcessing)

## 3] The Genetic algorithm

It's the final goal of the project : use both Image processing and command of the snake to find the best way for the snake to *move* when one of it's module is broken.

You may find more about image processing in [genetic_algo](./genetic_algo/) especially our generations results


