float2 c_add(float2 a, float2 b) {return (float2)(a.x+b.x,a.y+b.y);}
float2 c_sub(float2 a, float2 b) {return (float2)(a.x-b.x,a.y-b.y);}
float2 c_mul(float2 a, float2 b) {return (float2)(a.x*b.x-a.y*b.y,a.x*b.y+a.y*b.x);}
float2 c_div(float2 a, float2 b)
{
    float denominator=b.x*b.x+b.y*b.y;
    float2 factor=c_mul(a,(float2)(b.x,-b.y));
    return (float2)(factor.x/denominator,factor.y/denominator);
}
float2 c_div(float a, float2 b) {return c_div((float2)(a,0.0f),b);}
float2 c_div(float2 a, float b) {return c_div(a,(float2)(b,0.0f));}
float2 c_mul(float a, float2 b) {return c_mul((float2)(a,0.0f),b);}
float2 c_mul(float2 a, float b) {return c_mul(b,a);}
float2 c_add(float a, float2 b) {return c_add((float2)(a,0.0f),b);}
float2 c_add(float2 a, float b) {return c_add(b,a);}
float2 c_sub(float a, float2 b) {return c_sub((float2)(a,0.0f),b);}
float2 c_sub(float2 a, float b) {return c_sub(a,(float2)(b,0.0f));}
float2 c_sin(float2 x) {return (float2)(sin(x.x)*cosh(x.y),cos(x.x)*sinh(x.y));}
float2 c_cos(float2 x) {return (float2)(cos(x.x)*cosh(x.y),sin(x.x)*sinh(x.y));}
float2 c_exp(float2 z) {return (float2)(exp(z.x)*cos(z.y),exp(z.x)*sin(z.y));}