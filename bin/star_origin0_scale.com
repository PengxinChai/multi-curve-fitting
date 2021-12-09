#!/bin/tcsh -f
#####**************************************************************************#####
#Despcription: This program is used to generate a new star file in which the X,Y origins are scaled and shifted to be 0,0 by compensation of the X,Y coordinates in the micrographs.
#Copyright@MRC-LMB
#Author: Kai Zhang
#Last Edit: 2014-6-24

#####**************************************************************************#####

#global setup for output format
set KBold="\x1b\x5b1m"
set KDefault="\x1b\x5b0m"
set KUnderline="\x1b\x5b4m"
set KFlash="\x1b\x5b5m"

#end of global setup

set args = `printf "$argv" | wc | awk '{print $2}'`
set Proc_name=`echo $0 | awk '{n=split($1,scr,"/");print scr[n];}'`

if ( $args < 1 || $1 == '--help' || $1 == '-h' ) then

        printf "${KBold}Despcription: ${KDefault}This program is used to generate a new star file in which the X,Y origins are scaled and shifted to be 0,0 by compensation of the X,Y coordinates in the micrographs.\n"
        printf "              Then you can use the the new star file to extract particles again so that are particles should be well centered.\n"
        printf "              Make sure the star file contains  _rlnOriginX  _rlnOriginY   _rlnCoordinateX _rlnCoordinateY  columns.\n"

        printf "${KBold}Usage:${KDefault}   $Proc_name <scale factor> <star file1> <star file2> ...\n"
        printf "${KBold}example:${KDefault} $Proc_name 0.85 r3d2_cls2_data.star  \n"
        printf "${KBold}example:${KDefault} $Proc_name 1.66 r3d2_cls*_data.star  \n"

        exit(1)
endif


set scale=$1

set i=2

while ($i <= $args )
#<<< star while 1000

set starf=$argv[$i]
set root=`basename $starf .star`
set starf_new=${root}_origin0.star

if ( -f ${root}.star) then
set rlnOriginXIndex=`gawk 'NR<50 && /_rlnOriginX/{print $2}' $starf  |cut -c 2- `
set rlnOriginYIndex=`gawk 'NR<50 && /_rlnOriginY/{print $2}' $starf |cut -c 2- `
set rlnCoordinateXIndex=`gawk 'NR<50 && /_rlnCoordinateX/{print $2}' $starf  |cut -c 2- `
set rlnCoordinateYIndex=`gawk 'NR<50 && /_rlnCoordinateY/{print $2}' $starf  |cut -c 2- `

if ( $rlnOriginXIndex == "" || $rlnOriginYIndex == "" || $rlnCoordinateXIndex == "" || $rlnCoordinateYIndex == "") then
echo "Make sure the star file contains  _rlnOriginX  _rlnOriginY   _rlnCoordinateX _rlnCoordinateY  columns."
exit
endif

#get line number of head of Relion star file
set headN=`gawk '{if($2 ~ /#/)N=NR;}END{print N}' $starf `
gawk 'NR <= '$headN'' $starf > $starf_new

gawk '$'$rlnCoordinateXIndex'~/[0-9]/ && $'$rlnCoordinateYIndex'~/[0-9]/ && $'$rlnOriginXIndex'~/[0-9]/ && $'$rlnOriginYIndex'~/[0-9]/ { for(i=1;i<=NF;i++){ if( i=='$rlnCoordinateXIndex') printf("%d  ", 0.5 + ($i) - $'$rlnOriginXIndex' * '$scale' ); else if( i=='$rlnCoordinateYIndex') printf("%d  ", 0.5 + ($i) - $'$rlnOriginYIndex' * '$scale' );  else if( i=='$rlnOriginXIndex' || i=='$rlnOriginYIndex' ) printf("0  "); else    printf("%s  ", $i); }  printf("\n");}' $starf >>  $starf_new

#gawk '$'$rlnCoordinateXIndex'~/[0-9]/ && $'$rlnCoordinateYIndex'~/[0-9]/ {printf("%d\t%d\t%d\t%f\n", ($'$rlnCoordinateXIndex')*'$shrink'  , ($'$rlnCoordinateYIndex' ) *'$shrink', $'$rlnClassNumberIndex' , $'$rlnAutopickFigureOfMeritIndex')}' $box >>  $starf

echo "transforming $argv[$i] to $starf_new "
else
echo "$starf does not exists, or wrong format or suffix not .star"
endif

@ i++

end
#>>> end while 1000

