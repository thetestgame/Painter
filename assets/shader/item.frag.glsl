#version 130

// Texture inputs
uniform sampler2D p3d_Texture0; // Detail
uniform sampler2D p3d_Texture1; // Mask

// RGB inputs
uniform vec3 pnt_RedChannel;
uniform vec3 pnt_GreenChannel;
uniform vec3 pnt_BlueChannel;

// CMY inputs
uniform vec3 pnt_CyanChannel;
uniform vec3 pnt_MagentaChannel;
uniform vec3 pnt_YellowChannel;

// Backout inputs
uniform vec3 pnt_BlackoutChannel;

// Shader Input/Output
in vec2 texcoord;
out vec4 p3d_FragColor;

void main() {
  vec4 detail = texture(p3d_Texture0, texcoord);
  vec4 mask = texture(p3d_Texture1, texcoord);

  // Calculate Red Channel
  float red_channel = clamp(mask.r - (mask.g + mask.b), 0, 1);
  vec3 red_channel_color = red_channel * pnt_RedChannel;

  // Calculate Green Channel
  float green_channel = clamp(mask.g - (mask.r + mask.b), 0, 1);
  vec3 green_channel_color = green_channel * pnt_GreenChannel;

  // Calculate Blue Channel
  float blue_channel = clamp(mask.b - (mask.r + mask.g), 0, 1);
  vec3 blue_channel_color = blue_channel * pnt_BlueChannel;

  // Calculate Cyan Channel
  float cyan_channel = clamp(min(mask.b, mask.g), 0, 1);
  vec3 cyan_channel_color = cyan_channel * pnt_CyanChannel;

  // Calculate Magenta Channel
  float magenta_channel = clamp(min(mask.r, mask.b), 0, 1);
  vec3 magenta_channel_color = magenta_channel * pnt_MagentaChannel;

  // Calculate Yellow Channel
  float yellow_channel = clamp(min(mask.r, mask.g), 0, 1);
  vec3 yellow_channel_color = yellow_channel * pnt_YellowChannel;

  // Create final output color
  vec3 final_color = vec3(0);
  final_color += red_channel_color + green_channel_color + blue_channel_color;
  final_color += cyan_channel_color + magenta_channel_color + yellow_channel_color;
  final_color = final_color + dot(detail.rgb, vec3(0.1));

  // Calculate blackout colors
  float blackout = red_channel + green_channel + blue_channel;
  blackout += cyan_channel + magenta_channel + yellow_channel;
  blackout = 1 - blackout;
  vec3 blackout_color = blackout * pnt_BlackoutChannel * 0.8;
  blackout_color *= detail.rgb;

  // Export the final render color to the quad
  vec3 final_output = detail.rgb * final_color;
  final_output += blackout_color;
  p3d_FragColor = vec4(final_output, detail.a);
}