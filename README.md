# autorpg
Autotyper and captcha checker for EpicRPG
Uses a fixed image and compares it to a screensnip of the current screen. Returns a confidence interval and executes timed commands as to automatize EpicRPG on Discord platform.
Next step is ditching the fixed image comparison, gathering data and training a TensorFlow neural network to allow this project to branch out to different applications. Since 
even in EpicRPG the images change a bit, not always will we get 95%+ confidence, and sometimes if the random image differs too much from the expected image, the application
will fail the captcha (but get out of jail successfully, it´s just an efficiency problem).

Using a trained NN should alleviate these problems.
