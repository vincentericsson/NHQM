float2 integrand(float2 r, float2 k, float2 k_prime, float2 step)
{
    int l=1;
    float j=1.5;
     return c_mul(c_mul(    c_mul(r,r),   j_l(l,c_mul(k,r))   ), c_mul(j_l(l,c_mul(k_prime,r)),  V(r,j)));
    //return V(r,j);
    //return                     r*r *   j_l(l,      k*r)     *       j_l(l,      k_prime*r) *  V(r, j);
    // return 1.0f;  // testline, can probably be removed soon.
}

float2 get_element(int x, float2 k, float2 k_prim, float2 w, float2 start, float2 end, int n)
{
    float mass=0.019272;
    float2 sum=(float2)(0.0,0.0);
    // float step=(end-start)/((float2)(n,0));
    float2 step = c_div(c_sub(end,start),(float2)(n,0.0f));
    float2 xx=c_mul((float2)((float)(x%n)     ,0.0f),step);
    float2 yy=c_mul((float2)((float)((x-x%n)/n),0.0f),step);
    for (int i=0;i<25;i++)
    {
        sum=c_add(sum,   c_mul(get_gauss_legendre_w_25(i),integrand( c_mul((end-start)/2.0f,get_gauss_legendre_x_25(i)) + (start+end)/2.0f, xx,yy,step))      );
        //sum += (get_gauss_legendre_w_25(i) *     integrand( ((end-start)/2.0)*get_gauss_legendre_x_25(i) + (start+end)/2.0, xx, yy, step));
    }
    float2 integral=c_div(c_mul(c_sub(end,start),sum),(float2)(2.0f,0.0f));
    float2 diagonal=c_div(c_mul(xx,xx),(float2)(((2*mass)*((x%n)==((x-x%n)/n))),0.0f));
    // float2 diagonal=to_i(1.0f);
    // float diagonal=         (xx*xx)/         (2*mass)*((x%n)==((x-x%n)/n));
    // // return c_add(diagonal,c_mul(c_mul(yy,yy),c_mul(c_mul(step,integral),(float2)(2.0f/PI,0.0f))));
    return sum;
    // return    diagonal+           (yy*yy)*            step*integral*         2.0f/PI;
}