      program tcr
*
*     2019/02/07 for FOD
*     2019/12/10 for SOD
*     2020/11/19 for FGD
*     2021/02/05 for FGD
*
      integer nvar, nt, nite
      real    dt, xmiss, cs, cd

      parameter ( nvar = 5, nt = 201, nite = 1000 )
      parameter ( dt = 1. )
      parameter ( xmiss = -999. )

* Geoffroy et al. 2013
c      parameter ( cs = 8.2 )    !! CMIP5 MME mean upper layer heat capacity
c      parameter ( cd = 109. )    !! CMIP5 MME mean deeper layer heat capacity
* Smith et al. 2020
      parameter ( cs = 8.2075 ) !! CMIP6 MME mean upper layer heat capacity
      parameter ( cd = 97.6382 ) !! CMIP6 MME mean deeper layer heat capacity

      real    erf( nvar )
      real    fdb( nvar )
      real    ecs( nvar )
      real    gamma( nvar )
      real    eps( nvar )
      real    epsgamma( nvar )

      real    df( nvar )

      real    frc1( nvar )
      real    frc2( nvar )
      real    tstep( nvar )     !! T for step 2xCO2
      real    t1ppt( nvar )     !! T for 1%
      real    tstep_bak( nt,nvar )     !! T for step 2xCO2
      real    t1ppt_bak( nt,nvar )     !! T for 1%

      real    tcrout( nvar )       !! TCR
      real    dum( nvar )

      real    t
      real    b, b_ast, delta, phi_f, phi_s
      real    tau_f, tau_s, af, as, fact1, fact2, fact3
      real    x1, y1, z1, x2, y2, z2
      integer m, n, i, j, ite

* see the bottom for .ctl files
      character cfo(3)*90
      data cfo(1)
     &/'./erf_evolution.grd'/
      data cfo(2)
     &/'./ecs_evolution.grd'/
      data cfo(3)
     &/'./tcr_evolution.grd'/

*     vars: 5%, 17%, mean, 83%, 95%
      data  erf                 !! 2xCO2
     &     / 3.5, 3.698, 4.0, 4.302, 4.5 / !! FGD
      data  fdb                 !! lambda from process (sign reversed)
     &     / 1.8131, 1.5395, 1.1608, 0.7821, 0.5085 /!! FGD 
      data  ecs                 !! ECS from process
     &     / 2.15, 2.54, 3.44, 5.23, 7.81 /!! FGD 
      data  gamma               !! CMIP6 gamma
     &     / 0.4161, 0.4958, 0.6177, 0.7397, 0.8193 /
      data  eps                 !! CMIP6 epsiron
     &     / 0.8336, 1.0227, 1.3123, 1.6018, 1.7910 /
      data  epsgamma            !! CMIP6 epsiron x gamma
     &     / 0.3688, 0.5450, 0.8148, 1.0845, 1.2607 /

      open ( 91, file=cfo(1), form='unformatted' )
      open ( 92, file=cfo(2), form='unformatted' )
      open ( 93, file=cfo(3), form='unformatted' )
*
      do m = 1, nvar
         df( m ) = erf( m ) / 70.
      enddo
*
      dum = xmiss
*
*     ERF
*
      write( 6,* ) 
     &     ' @@@ ERF '

      t = 0.
      frc1 = 0.
      frc2 = 0.
      do n = 1, nt
         t = dt * real( n-1 )
         do m = 1, nvar
            frc1( m ) = erf( m ) !! F2xCO2
            frc2( m ) = df( m ) * t !! F(t)
            if( t .ge. 70. ) frc2( m ) = frc1( m )
         enddo
         do m = 1, nvar
            write( 91 ) frc1( m )
         enddo
         do m = 1, nvar
            write( 91 ) frc2( m )
         enddo
      enddo
*
*     ECS & TCR (varying F and lambda only)
*
      write( 6,* ) 
     &     ' @@@ ECS & TCR (varying F and lambda only) '

      t = 0.
      tstep = 0.
      t1ppt = 0.
      do n = 1, nt
         t = dt * real( n-1 )

         do m = 1, nvar

            b = ( fdb( m ) + epsgamma( 3 ) ) / cs 
     &           + epsgamma( 3 ) / cd / eps( 3 )
            b_ast = ( fdb( m ) + epsgamma( 3 ) ) / cs 
     &           - epsgamma( 3 ) / cd / eps( 3 )
            delta = b**2 - 4. * ( fdb( m )*epsgamma( 3 ) )
     &           / ( cs * cd * eps( 3 ) )
            phi_f = cs * ( b_ast - sqrt( delta ) ) / 2. / epsgamma( 3 )
            phi_s = cs * ( b_ast + sqrt( delta ) ) / 2. / epsgamma( 3 )
            tau_f = cs * cd * eps( 3 ) * ( b - sqrt( delta ) ) 
     &           / ( 2.*fdb( m )*epsgamma( 3 ) )
            tau_s = cs * cd * eps( 3 ) * ( b + sqrt( delta ) ) 
     &           / ( 2.*fdb( m )*epsgamma( 3 ) )
            af = fdb( m ) / cs - 1. / tau_s
            af = af * ( tau_f * tau_s ) / ( tau_s - tau_f )
            as = 1. - af
            fact1 = af * exp( -t/tau_f )
     &           + as * exp( -t/tau_s )
            fact2 = tau_f * af * ( 1. - exp( -t/tau_f ) ) 
     &            + tau_s * as * ( 1. - exp( -t/tau_s ) )
            fact3 = tau_f * af * ( 1. - exp( -70./tau_f ) )
     &                         * exp( -( t-70. )/tau_f ) 
     &            + tau_s * as * ( 1. - exp( -70./tau_s ) )
     &                         * exp( -( t-70. )/tau_s ) 

            tstep( m ) = ecs( m ) * ( 1. - fact1 ) !! F2xCO2 / lambda
            t1ppt( m ) = ecs( m ) * df( m ) / erf( m )
     &                   * ( t - fact2 )
            if( t .gt. 70. ) then
               t1ppt( m ) = ecs( m ) * ( 1. - df( m )/erf( m )*fact3 )
            endif

            if( n .gt. 140 ) then
               tstep( m ) = ecs( m )
               t1ppt( m ) = xmiss
            else if( n .gt. 130 ) then
               tstep( m ) = xmiss
               t1ppt( m ) = xmiss
            endif

         enddo
         do m = 1, nvar
            write( 92 ) tstep( m )
         enddo
         do m = 1, nvar
            write( 92 ) t1ppt( m )
         enddo

         do m = 1, nvar
            tstep_bak( n,m ) = tstep( m )
            t1ppt_bak( n,m ) = t1ppt( m )
         enddo

         if( n .eq. 70 ) then
            write( 6,* ) 
     &           '    TCR (5%, 17%, mean, 83%, 95%) = '
            write( 6,* ) t1ppt
         endif

      enddo                     !! n
*
*     ECS & TCR (varying F and lambda, and epsiron & gamma)
*
      write( 6,* )
     &     ' @@@ ECS & TCR (varying F and lambda, and epsiron & gamma) '

      t = 0.
      tstep = 0.
      t1ppt = 0.
      do n = 1, nt
         t = dt * real( n-1 )

         do m = 1, nvar

            b = ( fdb( 3 ) + epsgamma( m ) ) / cs 
     &           + epsgamma( m ) / cd / eps( m )
            b_ast = ( fdb( 3 ) + epsgamma( m ) ) / cs 
     &           - epsgamma( m ) / cd / eps( m )
            delta = b**2 - 4. * ( fdb( 3 )*epsgamma( m ) )
     &           / ( cs * cd * eps( m ) )
            phi_f = cs * ( b_ast - sqrt( delta ) ) / 2. / epsgamma( m )
            phi_s = cs * ( b_ast + sqrt( delta ) ) / 2. / epsgamma( m )
            tau_f = cs * cd * eps( m ) * ( b - sqrt( delta ) ) 
     &           / ( 2.*fdb( 3 )*epsgamma( m ) )
            tau_s = cs * cd * eps( m ) * ( b + sqrt( delta ) ) 
     &           / ( 2.*fdb( 3 )*epsgamma( m ) )
            af = fdb( 3 ) / cs - 1. / tau_s
            af = af * ( tau_f * tau_s ) / ( tau_s - tau_f )
            as = 1. - af
            fact1 = af * exp( -t/tau_f )
     &           + as * exp( -t/tau_s )
            fact2 = tau_f * af * ( 1. - exp( -t/tau_f ) ) 
     &            + tau_s * as * ( 1. - exp( -t/tau_s ) )
            fact3 = tau_f * af * ( 1. - exp( -70./tau_f ) )
     &                         * exp( -( t-70. )/tau_f ) 
     &            + tau_s * as * ( 1. - exp( -70./tau_s ) )
     &                         * exp( -( t-70. )/tau_s ) 

            tstep( m ) = ecs( 3 ) * ( 1. - fact1 ) !! F2xCO2 / lambda
            t1ppt( m ) = ecs( 3 ) * df( 3 ) / erf( 3 )
     &                   * ( t - fact2 )
            if( t .gt. 70. ) then
               t1ppt( m ) = ecs( 3 ) * ( 1. - df( 3 )/erf( 3 )*fact3 )
            endif

            if( n .gt. 140 ) then
               tstep( m ) = ecs( m )
               t1ppt( m ) = xmiss
            else if( n .gt. 130 ) then
               tstep( m ) = xmiss
               t1ppt( m ) = xmiss
            endif

         enddo                  !! m
*
*     multiply uncertainty
*
         if( n .le. 130 ) then
            do m = 1, nvar 
               x1 = tstep_bak( n,m ) - tstep( 3 )
               y1 = tstep( m ) - tstep( 3 )
               z1 = sqrt( x1**2 + y1**2 )
               x2 = t1ppt_bak( n,m ) - t1ppt( 3 )
               y2 = t1ppt( m ) - t1ppt( 3 )
               z2 = sqrt( x2**2 + y2**2 )
               if( m .lt. 3 ) then
                  tstep( m ) = tstep( 3 ) - z1
                  t1ppt( m ) = t1ppt( 3 ) - z2
               else if( m .gt. 3 ) then
                  tstep( m ) = tstep( 3 ) + z1
                  t1ppt( m ) = t1ppt( 3 ) + z2
               endif
            enddo
         endif

         do m = 1, nvar
            write( 93 ) tstep( m )
         enddo
         do m = 1, nvar
            write( 93 ) t1ppt( m )
         enddo
         do m = 1, nvar
            if( n .lt. 130 ) then
               write( 93 ) dum( m )
            elseif( n .lt. 140 ) then
               write( 93 ) tcrout( m )
            elseif( n .eq. 140 ) then
               write( 93 ) dum( m )
            else
               write( 93 ) ecs( m )
            endif
         enddo

         if( n .eq. 70 ) then
            do m = 1, nvar
               tcrout( m ) = t1ppt( m )
            enddo
            write( 6,* ) 
     &           '    TCR (5%, 17%, mean, 83%, 95%) = '
            write( 6,* ) t1ppt
         endif

      enddo                     !! n
*
      close( 91 )
      close( 92 )
      close( 93 )

      stop
      end
********************************
* .ctl file (copy and delete * below)
* 
* ZDEF:
* z=1  5%ile
* z=2  17%ile
* z=3  mean
* z=4  83%ile
* z=5  95%ile
* TDEF: year
* t=>141 is ECS
********************************
*dset ^erf_evolution.grd
*options sequential
*undef -999.
*title ERF
*ydef 1     linear -90.000000 1.25
*xdef 1     linear 0.000000 1.250000
*zdef 5     linear 1 1
*tdef 201  linear 00Z01Jan0000 1yr
*vars 2
*f1     5 99 ERF 2xCO2
*f2     5 99 ERF time dependent
*ENDVARS
********************************
*dset ^ecs_evolution.grd
*options sequential
*undef -999.
*title ECS/TCR
*ydef 1     linear -90.000000 1.25
*xdef 1     linear 0.000000 1.250000
*zdef 5     linear 1 1
*tdef 201  linear 00Z01Jan000 1yr
*vars 2
*t1     5 99 temperature response to 2xCO2
*t2     5 99 temperature response to 1% increase
*ENDVARS
********************************
*dset ^tcr_evolution.grd
*options sequential
*undef -999.
*title TCR
*ydef 1     linear -90.000000 1.25
*xdef 1     linear 0.000000 1.250000
*zdef 5     linear 1 1
*tdef 201  linear 00Z01Jan000 1yr
*vars 3
*t1     5 99 temperature response to 2xCO2
*t2     5 99 temperature response to 1% increase
*tf     5 99 temperature response (TCR & ECS)
*ENDVARS

