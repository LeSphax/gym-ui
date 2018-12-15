This repo contains three gym environments to train agents to click on a button based on visual input.

### Installation

Clone the repository and install the dependencies: 
```
git clone git@github.com:LeSphax/gym-ui.git
cd gym-ui
pip3 install -e .
```

### RandomButton-v0: 

Train an AI to click on a button that appears at a random position on the screen.
When the agent successfully clicks the button it gets a reward of 1 otherwise no reward, then the button is moved to a new random position.

### FixedButton-v0: 
Same environment as RandomButton-v0 but the buttons always appear at the same position

### FixedButtonHard-v0: 
Same environment as FixedButton-v0 but the buttons are smaller 

My initial idea was that this would be a first step to see if it would be possible 
to train agents to explore a User Interface using only curiosity-driven exploration.
Training agents to perform this simple task turned out to be more difficult than I thought.

I am not currently working on this project anymore.

