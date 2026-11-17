
from manim import *

class NeuralNetScene(Scene):
    def construct(self):
        title = Text("Neural Network Forward Pass", font_size=36, color=BLUE).to_edge(UP)
        self.play(Write(title))

        # Layers
        input_layer = VGroup(*[Circle(radius=0.25, color=GREEN).set_fill(GREEN, opacity=0.5) for _ in range(4)]).arrange(DOWN, buff=0.4).shift(LEFT * 3)
        hidden_layer = VGroup(*[Circle(radius=0.25, color=BLUE).set_fill(BLUE, opacity=0.5) for _ in range(5)]).arrange(DOWN, buff=0.3)
        output_layer = VGroup(*[Circle(radius=0.25, color=RED).set_fill(RED, opacity=0.5) for _ in range(2)]).arrange(DOWN, buff=0.6).shift(RIGHT * 3)

        self.play(FadeIn(input_layer), FadeIn(hidden_layer), FadeIn(output_layer))

        # Connections
        lines = VGroup()
        for i in input_layer:
            for h in hidden_layer:
                lines.add(Line(i.get_right(), h.get_left(), stroke_width=1, color=GRAY_B))
        for h in hidden_layer:
            for o in output_layer:
                lines.add(Line(h.get_right(), o.get_left(), stroke_width=1, color=GRAY_B))

        self.play(Create(lines), run_time=2)
        self.wait(1)
