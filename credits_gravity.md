---
layout: page
title: "happy-mario"
permalink: /credits/gravity
---
<canvas data-v-2b5f3470="" class="rocks" width="1560" height="1540"></canvas>
<script data-v-2b5f3470="" id="vs-rocks" type="notjs">
    precision mediump float;
    attribute vec4 position;
    varying vec2 rockUv;
    varying vec2 uv;
    varying mat2 rotation;n
    uniform float time;
    uniform float angle;
    uniform vec2 offset;
    uniform vec2 resolution;

    mat2 rotate(float angle) {
      float s = sin(angle);
      float c = cos(angle);

      return mat2(
        c, -s,
        s, c
      );
    }

    void main() {
      float aspectRatio = resolution.y / resolution.x;
      vec2 pos = position.xy;
      rotation = rotate(angle);
      pos *= rotation;
      pos.x *= aspectRatio;
      vec2 adjOffset = vec2(offset.x * aspectRatio, offset.y);

      gl_Position = vec4(pos * 1.01 + adjOffset, 0, 1.0);
      rockUv = position.xy * 2.0 - .5;
    }
  </script>

<script data-v-2b5f3470="" id="fs-rocks" type="notjs">
    precision mediump float;

    varying mat2 rotation;
    varying vec2 rockUv;
    varying vec2 uv;

    uniform vec2 resolution;
    uniform float time;
    uniform sampler2D rock;
    uniform float angle;
    uniform vec2 offset;
    uniform vec2 rocksPos[4];

    void main() {
      vec2 uv = gl_FragCoord.xy / resolution - .5;
      uv.x *= resolution.x / resolution.y;

      vec4 color = texture2D(rock, rockUv * 2.0);

      color.rgb *= clamp(1.0 - distance(uv - .03, offset / 2.0) * 8.5, .20, 1.2);

      for (int i = 0; i < 4; i++) {
        vec2 rockShadow = vec2(rocksPos[i].x, rocksPos[i].y - .08) / 2.0;
        color.rgb *=  clamp(distance(uv, rockShadow) * 14.0, 0.5, 1.35) * vec3(1.0, .92, .91);
      }

      gl_FragColor = color;
    }
  </script>
  <script data-v-2b5f3470="" id="vs-post" type="notjs">
    precision mediump float;
    attribute vec2 position;
    uniform vec2 resolution;
    varying vec2 uv;

    void main() {
      uv = position;
      gl_Position = vec4(position, 0., 1.);
    }
  </script>
  <script data-v-2b5f3470="" id="fs-post" type="notjs">
    precision mediump float;
    uniform sampler2D scene;
    uniform sampler2D bg;
    uniform vec2 resolution;
    uniform float time;
    varying vec2 uv;

    float invLerp(float a, float b, float v) {
      return (v - a) / (b - a);
    }

    float rand(vec2 co){
      return fract(sin(dot(co, vec2(12.9898, 78.233))) * 43758.5453);
    }

    void main() {
      vec2 adjUv = uv / 2.0 + .5;

      vec2 bgUv = vec2(adjUv.x * min(resolution.x / resolution.y, 1.0), adjUv.y);
      vec2 heatUv = bgUv + smoothstep(0., .6, uv.y + .6) * .005 * sin(time * .8 + (uv.y + 1.0) * 8.5);

      vec4 bgColor = texture2D(bg, heatUv);

      float fogOpacity = .56 * max(0., invLerp(-.8, -1.0, -1.0 * uv.y - 1.8));
      fogOpacity *= 1.1 - step(-.8, uv.y);

      vec4 sceneColor = texture2D(scene, adjUv);
      float shadowColor = fogOpacity * texture2D(scene, vec2(adjUv.x, adjUv.y * -1.0) + vec2(0.0, .2)).a;
      bgColor.rgb *= 1.0 - shadowColor;

      vec4 color = mix(bgColor, sceneColor, sceneColor.a);

      gl_FragColor = color;
    }
  </script>