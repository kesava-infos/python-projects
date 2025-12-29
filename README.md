# Sound Amplifier

\name{sound_amplifier}
\alias{sound_amplifier}
\title{Real-Time Audio Amplifier with Noise Reduction}
\description{
A real-time audio pass-through application that captures microphone input,
applies gain and optional noise reduction, and outputs the processed audio
to a selected playback device.
}
\details{
This application uses callback-based digital signal processing (DSP)
to achieve low-latency audio amplification. The system is designed to run
continuously while providing real-time control via a graphical user interface.

The architecture consists of:
\itemize{
  \item Audio capture and playback using a full-duplex stream
  \item Real-time digital signal processing (gain and noise reduction)
  \item Threaded execution to prevent UI blocking
  \item GUI-based device and parameter selection
}

Noise reduction assumes stationary noise and applies spectral attenuation.
Gain is applied multiplicatively and clipped to prevent signal distortion.
}
\usage{
sound_amplifier()
}
\arguments{
None. The application is controlled entirely through the graphical interface.
}
\value{
This function does not return a value. It launches an interactive GUI
and runs until the application is closed by the user.
}
\section{Audio Processing}{
The audio pipeline operates as follows:
\enumerate{
  \item Capture mono audio from the selected input device
  \item Apply optional stationary noise reduction
  \item Apply gain amplification
  \item Clip signal to the range [-1.0, 1.0]
  \item Output processed audio to the selected output device
}
}
\section{User Interface}{
The graphical interface provides:
\itemize{
  \item Input device selection (microphone)
  \item Output device selection (speakers or headphones)
  \item Gain control slider (1× to 10×)
  \item Noise reduction toggle
  \item Start and Stop controls
}
}
\section{Threading Model}{
Audio processing runs in a background daemon thread.
This ensures uninterrupted audio streaming while the GUI
remains responsive to user interaction.
}
\section{Performance Considerations}{
\itemize{
  \item Block size affects latency and CPU usage
  \item Smaller buffers reduce latency but increase processing overhead
  \item Noise reduction increases CPU load
}
}
\author{
Developed as a real-time DSP demonstration using sounddevice,
NumPy, and Tkinter.
}
\seealso{
\code{\link[sounddevice]{Stream}},
\code{\link[numpy]{clip}}
}
\examples{
## Launch the application
sound_amplifier()
}
