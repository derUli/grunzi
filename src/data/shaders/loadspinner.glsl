/**
 * @author rah, inspired by jonobr1 / http://jonobr1.com/
 */

/*
 * Output circle colors at given center pos and radius
 */
vec4 circle(vec2 uv, vec2 center, float radius, vec3 color)
{
    // Get distance of point from center, get difference from given radius
	float d = length(center - uv) - radius;
	float t = clamp(d, 0.0, 1.0);

    // If point is smaller than radius, set color alpha to 1, otherwise 0
	return vec4(color, 1.0 - t);
}

/*
 * Your work here!
 */
float computeRadius(vec2 uv)
{
    float radius = 0.25 * iResolution.y;

    // Centered uv
    vec2 uvCenter = (2.0f * uv - iResolution.xy);
    // Get pixel angle around the center
    float a = atan(uvCenter.x,uvCenter.y) - iTime;

    radius +=  sin(iTime ) * triangle_wave((a - iTime)/ (3.14 * 2.f) * 5.f, 1.f, 1.f) * 250.f;

    return radius;
}

void mainImage( out vec4 fragColor, in vec2 fragCoord ) {

	vec2 uv = fragCoord.xy;
	vec2 center = iResolution.xy * 0.5;
	float radius = computeRadius(uv);

    // Background layer
	vec4 layer1 = vec4(rgb(0.0, 0.0, 0.0), 1.0);

	// Circle
	vec3 red = rgb(225.0, 50.0, 70.0);
	vec4 layer2 = circle(uv, center, radius, red);

	// Blend the two
	fragColor = mix(layer1, layer2, layer2.a);

}