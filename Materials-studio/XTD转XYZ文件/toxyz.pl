#!perl
# XTDbead2XYZ - Convert the XTD files containing beads into XYZ format
# Creator: Sobereva (sobereva@sina.com)
# Date:    2012-May-23

use strict;
use MaterialsScript qw(:all);

#open the multiframe trajectory structure file or die
my $doc = $Documents{"./300K_MD.xsd"};

if (!$doc) {die "no document";}


    # Open new xmol trajectory file
    my $xmolFile=Documents->New("trj.txt");
   
    #get atoms in the structure
    my $Beads = $doc->DisplayRange->Beads;
    my $NBeads=@$Beads;

        foreach my $Bead (@$Beads) {
            # write atom symbol and x-y-z- coordinates
            $xmolFile->Append(sprintf "%s %f  %f  %f \n",$Bead->Name, $Bead->X, $Bead->Y, $Bead->Z);
        }   
    #close trajectory file
    $xmolFile->Close;
