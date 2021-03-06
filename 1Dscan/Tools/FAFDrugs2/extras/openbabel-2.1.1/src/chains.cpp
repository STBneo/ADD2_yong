/**********************************************************************
chains.cpp - Parse for macromolecule chains and residues.
 
Copyright (C) 1998-2001 by OpenEye Scientific Software, Inc.
(original author, Roger Sayle, version 1.6, March 1998)
(modified by Joe Corkery, OpenEye Scientific Software, March 2001)
Some portions Copyright (C) 2001-2006 by Geoffrey R. Hutchison
 
This file is part of the Open Babel project.
For more information, see <http://openbabel.sourceforge.net/>
 
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.
 
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
***********************************************************************/

//////////////////////////////////////////////////////////////////////////////
// File Includes
//////////////////////////////////////////////////////////////////////////////
#include <openbabel/babelconfig.h>

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <ctype.h>
#include <map>

#include <openbabel/mol.h>
#include <openbabel/chains.h>

using namespace std;

//////////////////////////////////////////////////////////////////////////////
// Preprocessor Definitions
//////////////////////////////////////////////////////////////////////////////

//! The first available index for actual residues
//! 0, 1, 2 reserved for UNK, HOH, LIG
#define RESIDMIN       3
//! The maximum number of residue IDs for this code
#define RESIDMAX       32

//! An index of the residue names perceived during a run
//! 0, 1, and 2 reserved for UNK, HOH, LIG
static char ChainsResName[RESIDMAX][4] = {
  /*0*/ "UNK",  /*1*/ "HOH",  /*2*/ "LIG"
};

#define ATOMMINAMINO   4
#define ATOMMINNUCLEIC 50
#define MAXPEPTIDE     11
#define MAXNUCLEIC     15
//! The number of amino acids recognized by this code
//! Currently: ILE, VAL, ALA, ASN, ASP, ARG, CYS, GLN, GLU
//!  GLY, HIS, HYP, LEU, LYS, MET, PHE, PRO, SER, THR, TRP, TYR
#define AMINOMAX       21
//! The number of nucleic acids recognized by this code
//! Currently A, C, T, G, U, I
#define NUCLEOMAX      6
#define STACKSIZE      20

#define AI_N           0
#define AI_CA          1
#define AI_C           2
#define AI_O           3
#define AI_OXT         37

#define AI_P           38
#define AI_O1P         39
#define AI_O2P         40
#define AI_O5          41
#define AI_C5          42
#define AI_C4          43
#define AI_O4          44
#define AI_C3          45
#define AI_O3          46
#define AI_C2          47
#define AI_O2          48
#define AI_C1          49

#define BitN           0x0001
#define BitNTer        0x0002
#define BitNPro        0x0004
#define BitNPT         0x0008
#define BitCA          0x0010
#define BitCAGly       0x0020
#define BitC           0x0100
#define BitCTer        0x0200
#define BitCOXT        0x0400
#define BitO           0x1000
#define BitOXT         0x2000

#define BitNAll        0x000F
#define BitCAAll       0x0030
#define BitCAll        0x0700
#define BitOAll        0x3000

#define BitP           0x0001
#define BitPTer        0x0002
#define BitOP          0x0004
#define BitO5          0x0008
#define BitO5Ter       0x0010
#define BitC5          0x0020
#define BitC4          0x0040
#define BitO4          0x0080
#define BitC3          0x0100
#define BitO3          0x0200
#define BitO3Ter       0x0400
#define BitC2RNA       0x0800
#define BitC2DNA       0x1000
#define BitO2          0x2000
#define BitC1          0x4000

#define BitPAll        0x0003
#define Bit05All       0x0018
#define BitO3All       0x0600
#define BitC2All       0x1800

#define BC_ASSIGN      0x01
#define BC_COUNT       0x02
#define BC_ELEM        0x03
#define BC_EVAL        0x04
#define BC_IDENT       0x05
#define BC_LOCAL       0x06

#define BF_SINGLE      0x01
#define BF_DOUBLE      0x02
#define BF_TRIPLE      0x04
#define BF_AROMATIC    0x08

namespace OpenBabel
{

  OBChainsParser chainsparser;

  //////////////////////////////////////////////////////////////////////////////
  // Structure / Type Definitions
  //////////////////////////////////////////////////////////////////////////////

  //! Structure template for atomic patterns in residues for OBChainsParser
  typedef struct Template
  {
    int flag;        //!< binary flag representing this atom type
    short elem;      //!< atomic number of this element
    short count;     //!< expected valence for this atom type
    int n1;          //!< mask 1 used by ConstrainBackbone() and MatchConstraint()
    int n2;          //!< mask 2 used by ConstrainBackbone() and MatchConstraint()
    int n3;          //!< mask 3 used by ConstrainBackbone() and MatchConstraint()
    int n4;          //!< mask 4 used by ConstrainBackbone() and MatchConstraint()
  }
  Template;

  //! Generic template for peptide residue backbone
  static Template Peptide[MAXPEPTIDE] = {
    /* N     */    {  0x0001, 7, 2, 0x0030, 0x0100,      0, 0 },
    /* NTer  */    {  0x0002, 7, 1, 0x0030,      0,      0, 0 },
    /* NPro  */    {  0x0004, 7, 3, 0x0030, 0x0100,     -6, 0 },
    /* NPT   */    {  0x0008, 7, 2, 0x0030,     -6,      0, 0 },
    /* CA    */    {  0x0010, 6, 3, 0x000F, 0x0700,     -6, 0 },
    /* CAGly */    {  0x0020, 6, 2, 0x0003, 0x0700,      0, 0 },
    /* C     */    {  0x0100, 6, 3, 0x0030, 0x1000, 0x0005, 0 },
    /* CTer  */    {  0x0200, 6, 2, 0x0030, 0x1000,      0, 0 },
    /* COXT  */    {  0x0400, 6, 3, 0x0030, 0x1000, 0x2000, 0 },
    /* O     */    {  0x1000, 8, 1, 0x0700,      0,      0, 0 },
    /* OXT   */    {  0x2000, 8, 1, 0x0400,      0,      0, 0 }
  };

  //! Generic template for peptide nucleotide backbone
  static Template Nucleotide[MAXNUCLEIC] = {
    /* P     */    {  0x0001, 15, 4, 0x0004, 0x0004, 0x0008, 0x0200 },
    /* PTer  */    {  0x0002, 15, 3, 0x0004, 0x0004, 0x0008,      0 },
    /* OP    */    {  0x0004,  8, 1, 0x0003,      0,      0,      0 },
    /* O5    */    {  0x0008,  8, 2, 0x0020, 0x0003,      0,      0 },
    /* O5Ter */    {  0x0010,  8, 1, 0x0020,      0,      0,      0 },
    /* C5    */    {  0x0020,  6, 2, 0x0018, 0x0040,      0,      0 },
    /* C4    */    {  0x0040,  6, 3, 0x0020, 0x0080, 0x0100,      0 },
    /* O4    */    {  0x0080,  8, 2, 0x0040, 0x4000,      0,      0 },
    /* C3    */    {  0x0100,  6, 3, 0x0040, 0x0600, 0x1800,      0 },
    /* O3    */    {  0x0200,  8, 2, 0x0100, 0x0001,      0,      0 },
    /* O3Ter */    {  0x0400,  8, 1, 0x0100,      0,      0,      0 },
    /* C2RNA */    {  0x0800,  6, 3, 0x0100, 0x4000, 0x2000,      0 },
    /* C2DNA */    {  0x1000,  6, 2, 0x0100, 0x4000,      0,      0 },
    /* O2    */    {  0x2000,  8, 1, 0x0800,      0,      0,      0 },
    /* C1    */    {  0x4000,  6, 3, 0x0080, 0x1800,     -7,      0 }
  };


  //////////////////////////////////////////////////////////////////////////////
  // Global Variables / Tables
  //////////////////////////////////////////////////////////////////////////////

  //! The number of PDB atom type names recognized by this code
#define ATOMMAX        68

  //! PDB atom types (i.e., columns 13-16 of a PDB file)
  //!  index numbers from this array are used in the pseudo-SMILES format
  //!  for side-chains in the AminoAcids[] & Nucleotides[] global arrays below
  static const char ChainsAtomName[ATOMMAX][4] = {
    /*  0 */  { ' ', 'N', ' ', ' ' },
    /*  1 */  { ' ', 'C', 'A', ' ' },
    /*  2 */  { ' ', 'C', ' ', ' ' },
    /*  3 */  { ' ', 'O', ' ', ' ' },
    /*  4 */  { ' ', 'C', 'B', ' ' },
    /*  5 */  { ' ', 'S', 'G', ' ' },
    /*  6 */  { ' ', 'O', 'G', ' ' },
    /*  7 */  { ' ', 'C', 'G', ' ' },
    /*  8 */  { ' ', 'O', 'G', '1' },
    /*  9 */  { ' ', 'C', 'G', '1' },
    /* 10 */  { ' ', 'C', 'G', '2' },
    /* 11 */  { ' ', 'C', 'D', ' ' },
    /* 12 */  { ' ', 'O', 'D', ' ' },
    /* 13 */  { ' ', 'S', 'D', ' ' },
    /* 14 */  { ' ', 'C', 'D', '1' },
    /* 15 */  { ' ', 'O', 'D', '1' },
    /* 16 */  { ' ', 'N', 'D', '1' },
    /* 17 */  { ' ', 'C', 'D', '2' },
    /* 18 */  { ' ', 'O', 'D', '2' },
    /* 19 */  { ' ', 'N', 'D', '2' },
    /* 20 */  { ' ', 'C', 'E', ' ' },
    /* 21 */  { ' ', 'N', 'E', ' ' },
    /* 22 */  { ' ', 'C', 'E', '1' },
    /* 23 */  { ' ', 'O', 'E', '1' },
    /* 24 */  { ' ', 'N', 'E', '1' },
    /* 25 */  { ' ', 'C', 'E', '2' },
    /* 26 */  { ' ', 'O', 'E', '2' },
    /* 27 */  { ' ', 'N', 'E', '2' },
    /* 28 */  { ' ', 'C', 'E', '3' },
    /* 29 */  { ' ', 'C', 'Z', ' ' },
    /* 30 */  { ' ', 'N', 'Z', ' ' },
    /* 31 */  { ' ', 'C', 'Z', '2' },
    /* 32 */  { ' ', 'C', 'Z', '3' },
    /* 33 */  { ' ', 'O', 'H', ' ' },
    /* 34 */  { ' ', 'N', 'H', '1' },
    /* 35 */  { ' ', 'N', 'H', '2' },
    /* 36 */  { ' ', 'C', 'H', '2' },
    /* 37 */  { ' ', 'O', 'X', 'T' },
    /* 38 */  { ' ', 'P', ' ', ' ' },
    /* 39 */  { ' ', 'O', '1', 'P' },
    /* 40 */  { ' ', 'O', '2', 'P' },
    /* 41 */  { ' ', 'O', '5', '*' },
    /* 42 */  { ' ', 'C', '5', '*' },
    /* 43 */  { ' ', 'C', '4', '*' },
    /* 44 */  { ' ', 'O', '4', '*' },
    /* 45 */  { ' ', 'C', '3', '*' },
    /* 46 */  { ' ', 'O', '3', '*' },
    /* 47 */  { ' ', 'C', '2', '*' },
    /* 48 */  { ' ', 'O', '2', '*' },
    /* 49 */  { ' ', 'C', '1', '*' },
    /* 50 */  { ' ', 'N', '9', ' ' },
    /* 51 */  { ' ', 'C', '8', ' ' },
    /* 52 */  { ' ', 'N', '7', ' ' },
    /* 53 */  { ' ', 'C', '5', ' ' },
    /* 54 */  { ' ', 'C', '6', ' ' },
    /* 55 */  { ' ', 'O', '6', ' ' },
    /* 56 */  { ' ', 'N', '6', ' ' },
    /* 57 */  { ' ', 'N', '1', ' ' },
    /* 58 */  { ' ', 'C', '2', ' ' },
    /* 59 */  { ' ', 'O', '2', ' ' },
    /* 60 */  { ' ', 'N', '2', ' ' },
    /* 61 */  { ' ', 'N', '3', ' ' },
    /* 62 */  { ' ', 'C', '4', ' ' },
    /* 63 */  { ' ', 'O', '4', ' ' },
    /* 64 */  { ' ', 'N', '4', ' ' },
    /* 65 */  { ' ', 'C', '5', ' ' },
    /* 66 */  { ' ', 'C', '5', 'M' },
    /* 67 */  { ' ', 'C', '6', ' ' }
  };

  //! Definition of side chains, associating overall residue name with
  //!  the pseudo-SMILES pattern
  typedef struct
  {
    const char *name; //!< Residue name, standardized by PDB
    const char *data; //!< pseudo-SMILES definition of side-chain
  }
  ResidType;

  //! Side chains for recognized amino acids using a pseudo-SMARTS syntax
  //!  for branching and bonds. Numbers indicate atom types defined by 
  //!  ChainsAtomName global array above
  static const ResidType AminoAcids[AMINOMAX] = {
    { "ILE", "1-4(-9-14)-10"                        },
    { "VAL", "1-4(-9)-10"                           },
    { "ALA", "1-4"                                  },
    { "ASN", "1-4-7(=15)-19"                        },
    { "ASP", "1-4-7(=15)-18"                        },
    { "ARG", "1-4-7-11-21-29(=34)-35"               },
    { "CYS", "1-4-5"                                },
    { "GLN", "1-4-7-11(=23)-27"                     },
    { "GLU", "1-4-7-11(=23)-26"                     },
    { "GLY", "1"                                    },
    { "HIS", "1-4-7^16~22^27^17~7"                  },
    { "HYP", "1-4-7(-12)-11-0"                      },
    { "LEU", "1-4-7(-14)-17"                        },
    { "LYS", "1-4-7-11-20-30"                       },
    { "MET", "1-4-7-13-20"                          },
    { "PHE", "1-4-7~14^22~29^25~17^7"               },
    { "PRO", "1-4-7-11-0"                           },
    { "SER", "1-4-6"                                },
    { "THR", "1-4(-8)-10"                           },
    { "TRP", "1-4-7~14^24^25~17(^7)^28~32^36~31^25" },
    { "TYR", "1-4-7~14^22~29(-33)^25~17^7"          }
  };
  // Other possible amino acid templates (less common)
  /* Pyroglutamate (PCA):        1-4-7-11(=" OE ")-0  PDB Example: 1CEL */
  /* Amino-N-Butyric Acid (ABA): 1-4-7                PDB Example: 1BBO */
  /* Selenic Acid (SEC):         1-4-"SEG "(-15)-18   PDB Example: 1GP1 */

  //! Side chains for recognized nucleotides using a pseudo-SMARTS syntax
  //!  for branching and bonds. Numbers indicate atom types defined by 
  //!  ChainsAtomName global array above
  static const ResidType Nucleotides[NUCLEOMAX] = {
    { "  A", "49-50-51-52-53-54(-56)-57-58-61-62(-53)-50"      },
    { "  C", "49-57-58(-59)-61-62(-64)-65-67-57"               },
    { "  G", "49-50-51-52-53-54(-55)-57-58(-60)-61-62(-53)-50" },
    { "  T", "49-57-58(-59)-61-62(-63)-65(-66)-67-57"          },
    { "  U", "49-57-58(-59)-61-62(-63)-65-67-57"               },
    { "  I", "49-50-51-52-53-54(-55)-57-58-61-62(-53)-50"      }
  };


  typedef struct
  {
    int atomid,elem;
    int bcount;
    int index;
  }
  MonoAtomType;

  typedef struct
  {
    int src,dst;
    int index;
    int flag;
  }
  MonoBondType;

  typedef struct
  {
    int type;
    union _ByteCode *next;
  }
  MonOpStruct;

  typedef struct
  {
    int type;
    int value;
    union _ByteCode *tcond;
    union _ByteCode *fcond;
  }
  BinOpStruct;

  //! Output array -- residue id, atom id, bond flags, etc.
  typedef struct
  {
    int type;
    int resid;
    int *atomid;
    int *bflags;
  }
  AssignStruct;

  //! Chemical graph matching virtual machine
  typedef union _ByteCode
  {
    int type;
    MonOpStruct eval;     //!< Eval - push current neighbors onto the stack
    BinOpStruct count;    //!< Count - test the number of eval bonds
    BinOpStruct elem;     //!< Element - test the element of current atom
    BinOpStruct ident;    //!< Ident - test the atom for backbone identity
    BinOpStruct local;    //!< Local - test whether the atom has been visited
    AssignStruct assign;  //!< Assign - assign residue name, atom name and bond type to output
  } ByteCode;

  typedef struct
  {
    int atom,bond;
    int prev;
  }
  StackType;

  static MonoAtomType MonoAtom[MaxMonoAtom];
  static MonoBondType MonoBond[MaxMonoBond];
  static int MonoAtomCount;
  static int MonoBondCount;

  static StackType Stack[STACKSIZE];
  static int StackPtr;

  static int  AtomIndex;
  static int  BondIndex;
  static bool StrictFlag = false;

  //////////////////////////////////////////////////////////////////////////////
  // Static Functions
  //////////////////////////////////////////////////////////////////////////////

  static ByteCode *AllocateByteCode(int type)
  {
    ByteCode *result;

    result = (ByteCode*)malloc(sizeof(ByteCode));
    if( !result )
      {
        obErrorLog.ThrowError(__FUNCTION__, "Unable to allocate byte codes for biomolecule residue perception.", obError);
        //        exit(1);
      }
    result->type = type;
    result->eval.next     = NULL;
    result->count.tcond   = NULL; 
    result->count.fcond   = NULL;
    result->elem.tcond    = NULL;
    result->elem.fcond    = NULL;
    result->ident.tcond   = NULL;
    result->ident.fcond   = NULL;
    result->local.tcond   = NULL;
    result->local.fcond   = NULL;
    result->assign.atomid = NULL;
    result->assign.bflags = NULL;

    return (result);
  }

  //! Free a ByteCode and all corresponding data
  static void DeleteByteCode(ByteCode *node)
  {
    if (node == NULL)
      return;
    else
      {
        switch (node->type)
          {
          case BC_ASSIGN:

            if (node->assign.atomid != NULL)
              free(node->assign.atomid);
            if (node->assign.bflags != NULL)
              free(node->assign.bflags);
            
            break;

          case BC_COUNT:

            DeleteByteCode(node->count.tcond);
            DeleteByteCode(node->count.fcond);
            break;
          case BC_ELEM:

            DeleteByteCode(node->elem.tcond);
            DeleteByteCode(node->elem.fcond);
            break;

          case BC_EVAL:

            DeleteByteCode(node->eval.next);
            break;

          case BC_IDENT:

            DeleteByteCode(node->ident.tcond);
            DeleteByteCode(node->ident.fcond);
            break;

          case BC_LOCAL:

            DeleteByteCode(node->local.tcond);
            DeleteByteCode(node->local.fcond);
            break;
          }

        free(node);
      }
  }

  static void FatalMemoryError(void)
  {
    obErrorLog.ThrowError(__FUNCTION__, "Unable to allocate memory for biomolecule residue / chain perception.", obError);
    //    exit(1);
  }

  void GenerateByteCodes(ByteCode **node, int resid, int curr, int prev, int bond)
  {
    StackType neighbour[4];
    StackType original;
    int count,i,j;
    ByteCode *ptr;
    bool done,found;

    if( curr != prev )
      {
        if( MonoAtom[curr].atomid < ATOMMINAMINO )
          {
            found = false;
            while( *node && ((*node)->type==BC_IDENT) )
              {
                if( (*node)->ident.value == MonoAtom[curr].atomid )
                  {
                    node  = (ByteCode**)&(*node)->ident.tcond;
                    found = true;
                    break;
                  }
                else
                  node = (ByteCode**)&(*node)->ident.fcond;
              }

            if (!found)
              {
                ptr = AllocateByteCode(BC_IDENT);
                ptr->ident.tcond = (ByteCode*)0;
                ptr->ident.fcond = *node;
                *node = ptr;
                node = (ByteCode**)&ptr->ident.tcond;
                ptr->ident.value = MonoAtom[curr].atomid;
              }
            MonoBond[bond].index = BondIndex++;
            done = true;
          }
        else if( MonoAtom[curr].index != -1 )
          {
            while( *node && ((*node)->type==BC_IDENT) )
              node = (ByteCode**)&(*node)->ident.fcond;

            found = false;
            while( *node && ((*node)->type==BC_LOCAL) )
              {
                if( (*node)->local.value == MonoAtom[curr].index )
                  {
                    node = (ByteCode**)&(*node)->local.tcond;
                    found = true;
                    break;
                  }
                else
                  node = (ByteCode**)&(*node)->local.fcond;
              }

            if (!found)
              {
                ptr = AllocateByteCode(BC_LOCAL);
                ptr->local.tcond = (ByteCode*)0;
                ptr->local.fcond = *node;
                *node = ptr;
                node = (ByteCode**)&ptr->local.tcond;
                ptr->local.value = MonoAtom[curr].index;
              }

            MonoBond[bond].index = BondIndex++;
            done = true;
          }
        else
          {
            while( *node && ((*node)->type==BC_IDENT) )
              node = (ByteCode**)&(*node)->ident.fcond;
            while( *node && ((*node)->type==BC_LOCAL) )
              node = (ByteCode**)&(*node)->local.fcond;

            found = false;
            while( *node && ((*node)->type==BC_ELEM) )
              {
                if( (*node)->elem.value == MonoAtom[curr].elem )
                  {
                    node = (ByteCode**)&(*node)->elem.tcond;
                    found = true;
                    break;
                  }
                else
                  node = (ByteCode**)&(*node)->elem.fcond;
              }

            if( !found )
              {
                ptr = AllocateByteCode(BC_ELEM);
                ptr->elem.tcond = (ByteCode*)0;
                ptr->elem.fcond = *node;
                *node = ptr;
                node = (ByteCode**)&ptr->elem.tcond;
                ptr->elem.value = MonoAtom[curr].elem;
              }

            MonoAtom[curr].index = AtomIndex++;
            MonoBond[bond].index = BondIndex++;
            done = false;
          }
      }
    else
      {
        MonoAtom[curr].index = AtomIndex++;
        done = false;
      }

    count = 0;
    if (!done)
      {
        for( i=0; i<MonoBondCount; i++ )
          {
            if( MonoBond[i].src == curr )
              {
                if( MonoBond[i].dst != prev )
                  {
                    neighbour[count].atom = MonoBond[i].dst;
                    neighbour[count].bond = i;
                    count++;
                  }
              }
            else if( MonoBond[i].dst == curr )
              {
                if( MonoBond[i].src != prev )
                  {
                    neighbour[count].atom = MonoBond[i].src;
                    neighbour[count].bond = i;
                    count++;
                  }
              }
          }

        if ( *node && ((*node)->type==BC_EVAL) )
          {
            found = false;
            node  = (ByteCode**)&(*node)->eval.next;
            while( *node && ((*node)->type==BC_COUNT) )
              {
                if( (*node)->count.value == count )
                  {
                    node = (ByteCode**)&(*node)->count.tcond;
                    found = true;
                    break;
                  }
                else
                  node = (ByteCode**)&(*node)->count.fcond;
              }

            if( !found )
              {
                ptr = AllocateByteCode(BC_COUNT);
                ptr->count.tcond = (ByteCode*)0;
                ptr->count.fcond = *node;
                *node = ptr;
                node = (ByteCode**)&ptr->count.tcond;
                ptr->count.value = count;
              }
          }
        else if( count || StrictFlag || StackPtr )
          {
            ptr = AllocateByteCode(BC_EVAL);
            ptr->eval.next = *node;
            *node = ptr;
            node = (ByteCode**)&ptr->eval.next;

            ptr = AllocateByteCode(BC_COUNT);
            ptr->count.tcond = (ByteCode*)0;
            ptr->count.fcond = *node;
            *node = ptr;
            node = (ByteCode**)&ptr->count.tcond;
            ptr->count.value = count;
          }
      }

    if( count == 1 )
      {
        GenerateByteCodes(node,resid,neighbour[0].atom, curr,neighbour[0].bond);
      }
    else if( count == 2 )
      {
        original = Stack[StackPtr++];
        Stack[StackPtr-1] = neighbour[0];
        Stack[StackPtr-1].prev = curr;
        GenerateByteCodes(node,resid,neighbour[1].atom,
                          curr,neighbour[1].bond);
        Stack[StackPtr-1] = neighbour[1];
        Stack[StackPtr-1].prev = curr;
        GenerateByteCodes(node,resid,neighbour[0].atom,
                          curr,neighbour[0].bond);
        Stack[--StackPtr] = original;
      }
    else if( count )
      {
        stringstream errorMsg;
        errorMsg << "Maximum Monomer Fanout Exceeded!" << endl;
        errorMsg << "Residue " << ChainsResName[resid] << " atom " 
                 << curr << endl;
        errorMsg << "Previous = " << prev << " Fanout = " << count << endl;
        obErrorLog.ThrowError(__FUNCTION__, errorMsg.str(), obWarning);
      }
    else if( StackPtr )
      {
        StackPtr--;
        GenerateByteCodes(node,resid,Stack[StackPtr].atom,
                          Stack[StackPtr].prev,Stack[StackPtr].bond);
        StackPtr++;
      }
    else if( !(*node) )
      {
        ptr = AllocateByteCode(BC_ASSIGN);
        ptr->assign.resid = resid;
        ptr->assign.atomid = (int*)malloc(AtomIndex*sizeof(int));
        if( !ptr->assign.atomid )
          FatalMemoryError();
        for( i=0; i<MonoAtomCount; i++ )
          if( (j=MonoAtom[i].index) != -1 )
            ptr->assign.atomid[j] = MonoAtom[i].atomid;
        if( BondIndex )
          {
            ptr->assign.bflags = (int*)malloc(BondIndex*sizeof(int));
            for( i=0; i<MonoBondCount; i++ )
              if( (j=MonoBond[i].index) != -1 )
                ptr->assign.bflags[j] = MonoBond[i].flag;
          }
        *node = ptr;
      }
    else if( (*node)->type == BC_ASSIGN )
      {
        if( (*node)->assign.resid != resid )
          {
            stringstream errorMsg;
            errorMsg << "Duplicated Monomer Specification!\n";
            errorMsg << "Residue " << ChainsResName[resid] 
                     << " matches residue ";
            errorMsg << ChainsResName[(*node)->assign.resid] << endl;
            obErrorLog.ThrowError(__FUNCTION__, errorMsg.str(), obWarning);
          }
      }

    /* Restore State! */
    if( curr != prev )
      {
        if( !done )
          {
            MonoAtom[curr].index = -1;
            AtomIndex--;
          }
        MonoBond[bond].index = -1;
        BondIndex--;
      }
  }

  //////////////////////////////////////////////////////////////////////////////
  // Constructors / Destructors
  //////////////////////////////////////////////////////////////////////////////

  // validated
  OBChainsParser::OBChainsParser(void) :
    bitmasks(NULL), visits(NULL), resids  (NULL), flags   (NULL),
    hetflags(NULL), atomids (NULL), resnos  (NULL), sernos  (NULL),
    hcounts (NULL), chains  (NULL)
  {
    int i, res = RESIDMIN;

    PDecisionTree = (ByteCode*)0;
    for( i=0 ; i < AMINOMAX ; i++ )
      {
        strncpy(ChainsResName[res],AminoAcids[i].name, sizeof(ChainsResName[res]) - 1);
        ChainsResName[res][sizeof(ChainsResName[res]) - 1] = '\0';
        DefineMonomer(&PDecisionTree,res,AminoAcids[i].data);
        res++;
      }

    NDecisionTree = (ByteCode*)0;
    for( i=0 ; i< NUCLEOMAX ; i++ )
      {
        strncpy(ChainsResName[res],Nucleotides[i].name, sizeof(ChainsResName[res]) - 1);
        ChainsResName[res][sizeof(ChainsResName[res]) - 1] = '\0';
        DefineMonomer(&NDecisionTree,res,Nucleotides[i].data);
        res++;
      }
  }

  OBChainsParser::~OBChainsParser(void)
  {
    DeleteByteCode((ByteCode*)PDecisionTree);
    DeleteByteCode((ByteCode*)NDecisionTree);
  }

  //////////////////////////////////////////////////////////////////////////////
  // Setup / Cleanup Functions
  //////////////////////////////////////////////////////////////////////////////

  //! Setup parsing for this molecule -- 
  void OBChainsParser::SetupMol(OBMol &mol)
  {
    CleanupMol();

    int i;
    int asize = mol.NumAtoms();
    int bsize = mol.NumBonds();

    bitmasks = new unsigned short[asize];
    visits   = new bool[asize];
    resids   = new unsigned char[asize];
    flags    = new unsigned char[bsize];
    hetflags = new bool[asize];
    atomids  = new int[asize];
    resnos   = new short[asize];
    sernos   = new short[asize];
    hcounts  = new char[asize];
    chains   = new char[asize];

    memset(bitmasks, 0,   sizeof(unsigned short) * asize);
    memset(visits,   0,   sizeof(bool)           * asize);
    memset(resids,   0,   sizeof(unsigned char)  * asize);
    memset(hetflags, 0,   sizeof(bool)           * asize);
    memset(resnos,   0,   sizeof(short)          * asize);
    memset(sernos,   0,   sizeof(short)          * asize);
    memset(hcounts,  0,   sizeof(char)           * asize);
    memset(chains,   ' ', sizeof(char)           * asize);
    
    memset(flags,    0,   sizeof(unsigned char)  * bsize);

    for ( i = 0 ; i < asize ; i++ )
      {
        atomids[i]  = -1;
      }
  }

  //! Clean up any molecular data left in memory -- frees all memory afterwards
  //! Used by OBChainsParser::SetupMol()
  void OBChainsParser::CleanupMol(void)
  {
    if (bitmasks != NULL)
      {
        delete bitmasks;
        bitmasks = NULL;
      }
    if (visits != NULL)
      {
        delete visits;
        visits = NULL;
      }
    if (hetflags != NULL)
      {
        delete hetflags;
        hetflags = NULL;
      }
    if (atomids  != NULL)
      {
        delete atomids;
        atomids = NULL;
      }
    if (resids   != NULL)
      {
        delete resids;
        resids = NULL;
      }
    if (resnos   != NULL)
      {
        delete resnos;
        resnos = NULL;
      }
    if (sernos   != NULL)
      {
        delete sernos;
        sernos = NULL;
      }
    if (hcounts  != NULL)
      {
        delete hcounts;
        hcounts = NULL;
      }
    if (chains   != NULL)
      {
        delete chains;
        chains = NULL;
      }
    if (flags    != NULL)
      {
        delete flags;
        flags = NULL;
      }
  }

  //! Clear all residue information for a supplied molecule
  void OBChainsParser::ClearResidueInformation(OBMol &mol)
  {
    OBResidue *residue;
    vector<OBResidue*> residues;
    vector<OBResidue*>::iterator r;

    for (residue = mol.BeginResidue(r) ; residue ; residue = mol.NextResidue(r))
      residues.push_back(residue);

    for ( unsigned int i = 0 ; i < residues.size() ; i++ )
      mol.DeleteResidue(residues[i]);

    residues.clear();
  }

  void OBChainsParser::SetResidueInformation(OBMol &mol, bool nukeSingleResidue)
  {
    char buffer[BUFF_SIZE];
    const char *symbol;
    string atomid, name;

    OBAtom    *atom;
    OBResidue *residue;
    map<short, OBResidue *> resmap;

    int size = mol.NumAtoms();
    for ( int i = 0 ; i < size ; i++ )
      {
        atom = mol.GetAtom(i+1); // WARNING: ATOM INDEX ISSUE

        if (atomids[i] == -1)
          {
            symbol = etab.GetSymbol(atom->GetAtomicNum());
            if( symbol[1] )
              {
                buffer[0] = symbol[0];
                buffer[1] = (char) toupper(symbol[1]);
              }
            else
              {
                buffer[0] = ' ';
                buffer[1] = symbol[0];
              }
            buffer[2] = ' ';
            buffer[3] = ' ';
            buffer[4] = '\0';
          }
        else if (atom->IsHydrogen())
          {
            if (hcounts[i])
              sprintf(buffer, "%cH%.2s", hcounts[i]+'0', ChainsAtomName[atomids[i]]+2);
            else
              sprintf(buffer, "H%.2s", ChainsAtomName[atomids[i]]+2);
          }
        else
          sprintf(buffer, "%.4s", ChainsAtomName[atomids[i]]);

        if (buffer[3] == ' ')
          buffer[3] = '\0';

        atomid = (buffer[0] == ' ') ? buffer + 1 : buffer;

        if (resmap.find(resnos[i]) != resmap.end())
          {
            residue = resmap[resnos[i]];
            residue->AddAtom(atom);
            residue->SetAtomID(atom, atomid);
            residue->SetHetAtom(atom, hetflags[i]);
            residue->SetSerialNum(atom, sernos[i]);
          }
        else
          {
            name    = ChainsResName[resids[i]];

            residue = mol.NewResidue();

            residue->SetName(name);
            residue->SetNum(resnos[i]);
            residue->SetChain(chains[i]);
            residue->SetChainNum((chains[i] > 'A') ? (int)(chains[i] - 'A') : 1);

            residue->AddAtom(atom);
            residue->SetAtomID(atom, atomid);
            residue->SetHetAtom(atom, hetflags[i]);
            residue->SetSerialNum(atom, sernos[i]);

            resmap[resnos[i]] = residue;
          }
      }

    if (mol.NumResidues() == 1 && nukeSingleResidue)
      mol.DeleteResidue(mol.GetResidue(0));
    else if (mol.NumResidues() == 1
             && (mol.GetResidue(0))->GetName() == "UNK")
      mol.DeleteResidue(mol.GetResidue(0));
  }

  //////////////////////////////////////////////////////////////////////////////
  // Perception Functions
  //////////////////////////////////////////////////////////////////////////////

  bool OBChainsParser::PerceiveChains(OBMol &mol, bool nukeSingleResidue)
  {
    bool result = true;

    SetupMol(mol);
    ClearResidueInformation(mol);

    result = DetermineHetAtoms(mol)          && result;
    result = DetermineConnectedChains(mol)   && result;
    result = DeterminePeptideBackbone(mol)   && result;
    result = DeterminePeptideSidechains(mol) && result;
    result = DetermineNucleicBackbone(mol)   && result;
    result = DetermineNucleicSidechains(mol) && result;
    result = DetermineHydrogens(mol)         && result;

    SetResidueInformation(mol, nukeSingleResidue);
    CleanupMol();

    obErrorLog.ThrowError(__FUNCTION__,
                          "Ran OpenBabel::PerceiveChains", obAuditMsg);

    return result;
  }

  /////////////////////////////////////////////////////////////////////////////
  // Hetero Atom Perception
  /////////////////////////////////////////////////////////////////////////////

  bool OBChainsParser::DetermineHetAtoms(OBMol &mol)
  {
    OBAtom *atom;
    vector<OBAtom *>::iterator a;
    for (atom = mol.BeginAtom(a) ; atom ; atom = mol.NextAtom(a))
      if (!atom->IsHydrogen() && atom->GetHvyValence() == 0)
        {
          // find un-connected atoms (e.g., HOH oxygen atoms)
          //  if it's not an oxygen, it's probably some ligand
          resids[atom->GetIdx()-1]   = (atom->IsOxygen()) ? 1 : 2;
          hetflags[atom->GetIdx()-1] = true;
        }
    return true;
  }

  /////////////////////////////////////////////////////////////////////////////
  // Connected Chain Perception
  /////////////////////////////////////////////////////////////////////////////

  bool OBChainsParser::DetermineConnectedChains(OBMol &mol)
  {
    int resid;
    int resno;
    int count;
    int size;
    int i,idx;
    int numAtoms;

    resno    = 1;
    count    = 0;
    numAtoms = mol.NumAtoms();

    OBAtom *atom;
    vector<OBAtom *>::iterator a;
    for (atom = mol.BeginAtom(a) ; atom ; atom = mol.NextAtom(a))
      {
        idx = atom->GetIdx() - 1;
        if (!hetflags[idx] && chains[idx] == ' ' && !atom->IsHydrogen())
          {
            size = RecurseChain(mol, idx, 'A' + count);
            
            // size = number of heavy atoms in residue chain
            if (size < 10) // small ligand, probably
              {
                if (size == 1 && atom->IsOxygen())
                  resid = 1; /* HOH */
                else
                  resid = 2; /* LIG */

                for (i = 0 ; i < numAtoms ; ++i)
                  {
                    if (chains[i] == ('A' + count))
                      {
                        hetflags[i] = true;
                        resids[i]   = resid;
                        resnos[i]   = resno;
                        chains[i]   = ' ';
                      }
                  }
                resno++;
              }
            else {
              count++; // number of connected chains
              if (count > 26) // out of chain IDs
                break;
            }
          }
      }

    if( count == 1 )
      for ( i = 0 ; i < numAtoms ; i++ )
        chains[i] = ' ';

    return true;
  }

  int OBChainsParser::RecurseChain(OBMol &mol, int i, int c)
  {
    OBAtom *atom, *nbr;
    vector<OBBond *>::iterator b;
    int result, index;

    atom      = mol.GetAtom(i+1);
    if (atom->IsHydrogen() )
      return 0;

    result    = 1;
    chains[i] = c;

    for (nbr = atom->BeginNbrAtom(b); nbr; nbr = atom->NextNbrAtom(b))
      {
        index = nbr->GetIdx() - 1;
        if (chains[index] == ' ')
          result += RecurseChain(mol, index,c);
      }

    return (result);
  }

  //////////////////////////////////////////////////////////////////////////////
  // Peptide Backbone Perception
  //////////////////////////////////////////////////////////////////////////////

  bool OBChainsParser::DeterminePeptideBackbone(OBMol &mol)
  {
    ConstrainBackbone(mol, Peptide, MAXPEPTIDE);

    int i, max = mol.NumAtoms();

    /* Order Peptide Backbone */

    for ( i = 0 ; i < max ; i++ )
      if (atomids[i] == -1)
        {
          if( bitmasks[i] & BitNTer )
            {
              atomids[i] = AI_N;
              TracePeptideChain(mol,i,1);
            }
          else if( (bitmasks[i]&BitNPT) && !(bitmasks[i]&BitN) )
            {
              atomids[i] = AI_N;
              TracePeptideChain(mol,i,1);
            }
        }

    /* Carbonyl Double Bond */

    OBBond *bond;
    vector<OBBond*>::iterator b;
    for (bond = mol.BeginBond(b) ; bond ; bond = mol.NextBond(b))
      {
        if ((atomids[bond->GetBeginAtomIdx()-1] == 2 && atomids[bond->GetEndAtomIdx()-1] == 3) ||
            (atomids[bond->GetBeginAtomIdx()-1] == 3 && atomids[bond->GetEndAtomIdx()-1] == 2))
          flags[bond->GetIdx()] |= BF_DOUBLE;
      }

    return true;
  }

  void OBChainsParser::ConstrainBackbone(OBMol &mol, Template *templ, int tmax)
  {
    static OBAtom *neighbour[6];
    Template *pep;
    OBAtom *na,*nb,*nc,*nd;
    OBAtom *atom, *nbr;
    bool change, result;
    int  count;
    int  i,idx;

    vector<OBAtom *>::iterator a;
    vector<OBBond *>::iterator b;

    /* First Pass */

    for (atom = mol.BeginAtom(a) ; atom ; atom = mol.NextAtom(a))
      {
        idx = atom->GetIdx() - 1;
        bitmasks[idx] = 0;
        for ( i = 0 ; i < tmax ; i++ )
          if ( (static_cast<unsigned int>(templ[i].elem)  == atom->GetAtomicNum())
               &&
               (static_cast<unsigned int>(templ[i].count) == atom->GetHvyValence()))
            bitmasks[idx] |= templ[i].flag;
      }

    /* Second Pass */

    do
      {
        change = false;
        for (atom = mol.BeginAtom(a) ; atom ; atom = mol.NextAtom(a))
          {
            idx = atom->GetIdx() - 1;
            if (bitmasks[idx]) // Determine Neighbours
              {
                count = 0;
                for (nbr = atom->BeginNbrAtom(b) ; nbr ; nbr = atom->NextNbrAtom(b))
                  if (!nbr->IsHydrogen())
                    neighbour[count++] = nbr;

                na = neighbour[0];
                nb = neighbour[1];
                nc = neighbour[2];
                nd = neighbour[3];

                for ( i = 0 ; i < tmax ; i++ )
                  if ( templ[i].flag & bitmasks[idx] )
                    {
                      pep    = &templ[i];
                      result = true;

                      if (count == 4)
                        result = Match4Constraints(pep,na,nb,nc,nd);
                      else if (count == 3)
                        result = Match3Constraints(pep,na,nb,nc);
                      else if (count == 2)
                        result = Match2Constraints(pep,na,nb);
                      else // count == 1
                        result = MatchConstraint(na,pep->n1);

                      if(result == false)
                        {
                          bitmasks[idx] &= ~pep->flag;
                          change = true;
                        }
                    }
              }
          }
      }
    while( change );
  }

  bool OBChainsParser::MatchConstraint(OBAtom *atom, int mask)
  {
    if (atom == NULL)
      return (false);

    if( mask < 0 )
      return(atom->GetAtomicNum() == static_cast<unsigned int>(-mask));
    else
      return(((bitmasks[atom->GetIdx()-1]&mask) == 0) ? false : true);
  }

  bool OBChainsParser::Match2Constraints(Template *tmpl, OBAtom *na, OBAtom *nb)
  {
    if (na == NULL || nb == NULL)
      return (false); // don't even try to evaluate it

    if( MatchConstraint(na,tmpl->n2) )
      if( MatchConstraint(nb,tmpl->n1) )
        return( true );
    if( MatchConstraint(nb,tmpl->n2) )
      if( MatchConstraint(na,tmpl->n1) )
        return( true );
    return( false );
  }

  bool OBChainsParser::Match3Constraints(Template *tmpl, OBAtom *na, OBAtom *nb, OBAtom *nc)
  {
    if (na == NULL || nb == NULL || nc == NULL)
      return (false); // don't even try to evaluate it

    if( MatchConstraint(na,tmpl->n3) )
      if( Match2Constraints(tmpl,nb,nc) )
        return( true );
    if( MatchConstraint(nb,tmpl->n3) )
      if( Match2Constraints(tmpl,na,nc) )
        return( true );
    if( MatchConstraint(nc,tmpl->n3) )
      if( Match2Constraints(tmpl,na,nb) )
        return( true );
    return( false );
  }

  bool OBChainsParser::Match4Constraints(Template *tmpl, OBAtom *na, OBAtom *nb, OBAtom *nc, OBAtom *nd)
  {
    if (na == NULL || nb == NULL || nc == NULL || nd == NULL)
      return (false); // don't even try to evaluate it

    if( MatchConstraint(na,tmpl->n4) )
      if( Match3Constraints(tmpl,nb,nc,nd) )
        return( true );
    if( MatchConstraint(nb,tmpl->n4) )
      if( Match3Constraints(tmpl,na,nc,nd) )
        return( true );
    if( MatchConstraint(nc,tmpl->n4) )
      if( Match3Constraints(tmpl,na,nb,nd) )
        return( true );
    if( MatchConstraint(nd,tmpl->n4) )
      if( Match3Constraints(tmpl,na,nb,nc) )
        return( true );
    return( false );
  }

  void OBChainsParser::TracePeptideChain(OBMol &mol, int i, int r)
  {
    int neighbour[4];
    int na,nb,nc;
    OBAtom *atom, *nbr;
    int count;
    int j,k,idx;

    vector<OBBond *>::iterator b;

    /* Determine Neighbours */

    atom = mol.GetAtom(i+1);
    idx  = atom->GetIdx() - 1;
    if (visits[i])
      return;
    visits[i] = true;

    count = 0;
    for (nbr = atom->BeginNbrAtom(b) ; nbr ; nbr = atom->NextNbrAtom(b))
      if (!nbr->IsHydrogen())
        neighbour[count++] = nbr->GetIdx()-1;

    resnos[idx] = r;

    na = neighbour[0];
    nb = neighbour[1];
    nc = neighbour[2];

    switch( atomids[i] )
      {
      case(AI_N):
        for( j=0; j<count; j++ )
          if (bitmasks[neighbour[j]] & BitCAAll)
            {
              atomids[neighbour[j]] = AI_CA;
              if (!visits[neighbour[j]])
                TracePeptideChain(mol,neighbour[j],r);
            }
        break;

      case(AI_CA):
        if( count == 3 )
          {
            if ( bitmasks[na] & BitNAll )
              na = nc;
            else if ( bitmasks[nb] & BitNAll )
              nb = nc;

            if ( bitmasks[na] & BitC )
              {
                j = na;
                k = nb;
              }
            else if ( bitmasks[nb] & BitC )
              {
                j = nb;
                k = na;
              }
            else if( bitmasks[na] & BitCAll )
              {
                j = na;
                k = nb;
              }
            else if (bitmasks[nb] & BitCAll )
              {
                j = nb;
                k = na;
              }

            atomids[j]  = AI_C;
            bitmasks[k] = 0;

              if (!visits[j])
                TracePeptideChain(mol,j,r);
          }
        else /* count == 2 */
          {
            if ( bitmasks[na] & BitCAll )
              {
                atomids[na] = AI_C;
                if (!visits[na])
                  TracePeptideChain(mol,na,r);
              }
            else if ( bitmasks[nb] & BitCAll )
              {
                atomids[nb] = AI_C;
                if (!visits[nb])
                  TracePeptideChain(mol,nb,r);
              }
          }
        break;

      case(AI_C):
        k = AI_O;
        for ( j = 0; j < count; j++ )
          {
            if ( bitmasks[neighbour[j]] & BitNAll )
              {
                atomids[neighbour[j]] = AI_N;
                if (!visits[neighbour[j]])
                  TracePeptideChain(mol,neighbour[j],r+1);
              }
            else if( bitmasks[neighbour[j]] & BitOAll )
              {
                atomids[neighbour[j]] = k;
                resnos[neighbour[j]]  = r;
                k = AI_OXT;  /* OXT */
              }
          }
        break;
      }
  }

  //////////////////////////////////////////////////////////////////////////////
  // Peptide Sidechains Perception
  //////////////////////////////////////////////////////////////////////////////

  bool OBChainsParser::DeterminePeptideSidechains(OBMol &mol)
  {
    int resid;
    int max = mol.NumAtoms();

    for (int i = 0 ; i < max ; ++i)
      if (atomids[i] == AI_CA)
        {
          resid = IdentifyResidue(PDecisionTree, mol, i, resnos[i]);
          AssignResidue(mol,resnos[i],chains[i],resid);
        }

    return true;
  }

  void OBChainsParser::AssignResidue(OBMol &mol, int r, int c, int i)
  {
    int max = mol.NumAtoms();

    for (int j = 0 ; j < max ; ++j)
      if ((resnos[j] == r) && (chains[j] == c) && !hetflags[j])
        resids[j] = i;
  }

  int OBChainsParser::IdentifyResidue(void *tree, OBMol &mol, int seed,
                                      int resno)
  {
    ByteCode *ptr;

    int AtomCount, BondCount;
    int curr,prev,bond;
    int bcount;
    int i,j;

    ptr    = (ByteCode *) tree;
    bcount = 0;

    Stack[0].atom = seed;
    Stack[0].prev = seed;
    StackPtr = 0;

    ResMonoAtom[0] = seed;
    AtomCount = 1;
    BondCount = 0;

    OBAtom *atom, *nbr;
    vector<OBBond *>::iterator b;

    while( ptr ) {
      switch(ptr->type)
        {
        case(BC_IDENT):  curr = Stack[StackPtr-1].atom;
          if( atomids[curr] == ptr->ident.value )
            {
              bond = Stack[StackPtr-1].bond;
              ResMonoBond[BondCount++] = bond;
              ptr = ptr->ident.tcond;
              StackPtr--;
            }
          else
            ptr = ptr->ident.fcond;
          break;

        case(BC_LOCAL):  curr = Stack[StackPtr-1].atom;
          if( curr == ResMonoAtom[ptr->local.value] )
            {
              bond = Stack[StackPtr-1].bond;
              ResMonoBond[BondCount++] = bond;
              ptr = ptr->local.tcond;
              StackPtr--;
            }
          else
            ptr = ptr->local.fcond;
          break;

        case(BC_ELEM):   curr = Stack[StackPtr-1].atom;
          if( mol.GetAtom(curr+1)->GetAtomicNum() == static_cast<unsigned int>(ptr->elem.value) )
            {
              bond = Stack[StackPtr-1].bond;
              ResMonoAtom[AtomCount++] = curr;
              ResMonoBond[BondCount++] = bond;
              resnos[curr] = resno;
              ptr = ptr->elem.tcond;
              StackPtr--;
            }
          else
            ptr = ptr->elem.fcond;
          break;

        case(BC_EVAL):   bcount = 0;
          curr = Stack[StackPtr].atom;
          prev = Stack[StackPtr].prev;

          atom = mol.GetAtom(curr+1); // WARNING, potential atom index issue
          for (nbr = atom->BeginNbrAtom(b); nbr; nbr = atom->NextNbrAtom(b))
            {
              if (nbr->IsHydrogen())
                continue;

              j = nbr->GetIdx() - 1;
              if (!((curr == prev) && bitmasks[j]) && (j != prev))
                {
                  Stack[StackPtr].prev = curr;
                  Stack[StackPtr].atom = j;
                  Stack[StackPtr].bond = (*b)->GetIdx();
                  StackPtr++;
                  bcount++;
                }
            }

          ptr = ptr->eval.next;
          break;

        case(BC_COUNT):
          if( bcount == ptr->count.value )
            {
              ptr = ptr->count.tcond;
            }
          else
            ptr = ptr->count.fcond;
          break;

        case(BC_ASSIGN): 
          for( i=0; i<AtomCount; i++ ) {
            if( !bitmasks[ResMonoAtom[i]])
              {
                j = ptr->assign.atomid[i];
                atomids[ResMonoAtom[i]] = j;
              }
          }
          for( i=0; i<BondCount; i++ )
            {
              j = ptr->assign.bflags[i];
              flags[ResMonoBond[i]] = j;
            }
          return( ptr->assign.resid );
          break;

        default:  /* Illegal Instruction! */
          return( 0 );
        } // (switch)
    } // while (loop through atoms)
    return 0;
  }

  //////////////////////////////////////////////////////////////////////////////
  // Nucleic Backbone Perception
  /////////////////////////////////////////////////////////////////////////////

  bool OBChainsParser::DetermineNucleicBackbone(OBMol &mol)
  {
    ConstrainBackbone(mol, Nucleotide, MAXNUCLEIC);

    int i, max = mol.NumAtoms();

    /* Order Nucleic Backbone */

    for( i = 0 ; i < max ; i++ )
      if( atomids[i] == -1 )
        {
          if( bitmasks[i] & BitPTer )
            {
              atomids[i] = AI_P;
              TraceNucleicChain(mol,i,1);
            }
          else if( bitmasks[i] & BitO5Ter )
            {
              atomids[i] = AI_O5;
              TraceNucleicChain(mol,i,1);
            }
        }

    return true;
  }

  void OBChainsParser::TraceNucleicChain(OBMol &mol, int i, int r)
  {
    int neighbour[4];
    int na,nb,nc;
    int count;
    int j,k;

    OBAtom *atom, *nbr;
    vector<OBBond *>::iterator b;

    if (visits[i])
      return;
    visits[i] = true;

    count = 0;
    atom  = mol.GetAtom(i + 1);
    for (nbr = atom->BeginNbrAtom(b) ; nbr ; nbr = atom->NextNbrAtom(b))
      if (!nbr->IsHydrogen())
        neighbour[count++] = nbr->GetIdx() - 1;

    resnos[i] = r;

    na = neighbour[0];
    nb = neighbour[1];
    nc = neighbour[2];

    switch( atomids[i] )
      {
      case(AI_P):
        k = AI_O1P;  /* O1P */
        for( j=0; j<count; j++ )
          {
            if( bitmasks[neighbour[j]] & BitO5 )
              {
                atomids[neighbour[j]] = AI_O5;
                if (!visits[neighbour[j]])
                  TraceNucleicChain(mol,neighbour[j],r);
              }
            else if( bitmasks[neighbour[j]] & BitOP )
              {
                atomids[neighbour[j]] = k;
                resnos[neighbour[j]]  = r;
                k = AI_O2P;  /* O2P */
              }
          }

        break;

      case(AI_O5):
        for( j=0; j<count; j++ )
          if( bitmasks[neighbour[j]] & BitC5 )
            {
              atomids[neighbour[j]] = AI_C5;
              if (!visits[neighbour[j]])
                TraceNucleicChain(mol,neighbour[j],r);
            }

        break;

      case(AI_C5):
        for( j=0 ; j<count; j++ )
          if( bitmasks[neighbour[j]] & BitC4 )
            {
              atomids[neighbour[j]] = AI_C4;
              if (!visits[neighbour[j]])
                TraceNucleicChain(mol,neighbour[j],r);
            }

        break;

      case(AI_C4):
        for( j=0; j<count; j++ )
          {
            if( bitmasks[neighbour[j]] & BitC3 )
              {
                atomids[neighbour[j]] = AI_C3;
                if (!visits[neighbour[j]])
                  TraceNucleicChain(mol,neighbour[j],r);
              }
            else if( bitmasks[neighbour[j]] & BitO4 )
              {
                atomids[neighbour[j]] = AI_O4;
                resnos[neighbour[j]]  = r;
              }
          }

        break;

      case(AI_C3):
        for( j=0; j<count; j++ )
          {
            if( bitmasks[neighbour[j]] & BitO3All )
              {
                atomids[neighbour[j]] = AI_O3;
                if (!visits[neighbour[j]])
                  TraceNucleicChain(mol,neighbour[j],r);
              }
            else if( bitmasks[neighbour[j]] & BitC2All )
              {
                atomids[neighbour[j]] = AI_C2;
                if (!visits[neighbour[j]])
                  TraceNucleicChain(mol,neighbour[j],r);
              }
          }

        break;

      case(AI_O3):
        for( j=0; j<count; j++ )
          if( bitmasks[neighbour[j]] & BitP )
            {
              atomids[neighbour[j]] = AI_P;
              if (!visits[neighbour[j]])
                TraceNucleicChain(mol,neighbour[j],r+1);
            }

        break;

      case(AI_C2):
        for( j=0; j<count; j++ )
          {
            if( bitmasks[neighbour[j]] & BitC1 )
              {
                atomids[neighbour[j]] = AI_C1;
                resnos[neighbour[j]]  = r;
              }
            else if( bitmasks[neighbour[j]] & BitO2 )
              {
                atomids[neighbour[j]] = AI_O2;
                resnos[neighbour[j]]  = r;
              }
          }

        break;
      }
  }

  //////////////////////////////////////////////////////////////////////////////
  // Nucleic Sidechains Perception
  //////////////////////////////////////////////////////////////////////////////

  bool OBChainsParser::DetermineNucleicSidechains(OBMol &mol)
  {
    for( unsigned int i = 0 ; i < mol.NumAtoms() ; i++ )
      if( atomids[i] == 49 )
        {
          int resid = IdentifyResidue(NDecisionTree,mol,i,resnos[i]);
          AssignResidue(mol,resnos[i],chains[i],resid);
        }

    return true;
  }

  //////////////////////////////////////////////////////////////////////////////
  // Hydrogens Perception
  //////////////////////////////////////////////////////////////////////////////

  bool OBChainsParser::DetermineHydrogens(OBMol &mol)
  {
    OBAtom *atom, *nbr;
    int idx,sidx;

    int max = mol.NumAtoms();
    for ( int i = 0 ; i < max ; i++ )
      hcounts[i] = 0;

    /* First Pass */

    vector<OBAtom*>::iterator a;
    vector<OBBond*>::iterator b;

    for(atom = mol.BeginAtom(a); atom ; atom = mol.NextAtom(a))
      if(atom->IsHydrogen())
        {
          nbr = atom->BeginNbrAtom(b);
          if (nbr != NULL)
            {
              idx  = atom->GetIdx() - 1;
              sidx = nbr->GetIdx() - 1;

              hcounts[idx]  = ++hcounts[sidx];
              hetflags[idx] = hetflags[sidx];
              atomids[idx]  = atomids[sidx];
              resids[idx]   = resids[sidx];
              resnos[idx]   = resnos[sidx];
            }
        }

    /* Second Pass */

    for(atom = mol.BeginAtom(a) ; atom ; atom = mol.NextAtom(a))
      if (atom->IsHydrogen())
        {
          nbr = atom->BeginNbrAtom(b);
          if (nbr != NULL && hcounts[nbr->GetIdx()-1] == 1)
            hcounts[atom->GetIdx()-1] = 0;
        }

    return true;
  }

  //////////////////////////////////////////////////////////////////////////////
  // Utility Functions
  //////////////////////////////////////////////////////////////////////////////

  // validated
  void OBChainsParser::DefineMonomer(void **tree, int resid, const char *smiles)
  {
    int i;

    MonoAtomCount = 0;
    MonoBondCount = 0;

    ParseSmiles(smiles,-1);

    for( i=0; i<MonoBondCount; i++ )
      MonoBond[i].index = -1;
    for( i=0; i<MonoAtomCount; i++ )
      MonoAtom[i].index = -1;
    AtomIndex = BondIndex = 0;

    StackPtr = 0;
    GenerateByteCodes((ByteCode**)tree, resid, 0, 0, 0 );
  }

  int OBChainsParser::IdentifyElement(const char *ptr)
  {
    int ch;

    ch = toupper(ptr[1]);
    switch( toupper(ptr[0]) )
      {
      case(' '):  switch( ch )
        {
        case('B'):  return(  5 );
        case('C'):  return(  6 );
        case('D'):  return(  1 );
        case('F'):  return(  9 );
        case('H'):  return(  1 );
        case('I'):  return( 53 );
        case('K'):  return( 19 );
        case('L'):  return(  1 );
        case('N'):  return(  7 );
        case('O'):  return(  8 );
        case('P'):  return( 15 );
        case('S'):  return( 16 );
        case('U'):  return( 92 );
        case('V'):  return( 23 );
        case('W'):  return( 74 );
        case('Y'):  return( 39 );
        }
        break;

      case('A'):  switch( ch )
        {
        case('C'):  return( 89 );
        case('G'):  return( 47 );
        case('L'):  return( 13 );
        case('M'):  return( 95 );
        case('R'):  return( 18 );
        case('S'):  return( 33 );
        case('T'):  return( 85 );
        case('U'):  return( 79 );
        }
        break;

      case('B'):  switch( ch )
        {
        case('A'):  return( 56 );
        case('E'):  return(  4 );
        case('I'):  return( 83 );
        case('K'):  return( 97 );
        case('R'):  return( 35 );
        case(' '):  return(  5 );
        }
        break;

      case('C'):  switch( ch )
        {
        case('A'):  return( 20 );
        case('D'):  return( 48 );
        case('E'):  return( 58 );
        case('F'):  return( 98 );
        case('L'):  return( 17 );
        case('M'):  return( 96 );
        case('O'):  return( 27 );
        case('R'):  return( 24 );
        case('S'):  return( 55 );
        case('U'):  return( 29 );
        case(' '):  return(  6 );
        }
        break;

      case('D'):  if( ch=='Y' )
        {
          return( 66 );
        }
      else if( ch==' ' )
        return( 1 );
        break;

      case('E'):  if( ch=='R' )
        {
          return( 68 );
        }
      else if( ch=='S' )
        {
          return( 99 );
        }
      else if( ch=='U' )
        return( 63 );
        break;

      case('F'):  if( ch=='E' )
        {
          return(  26 );
        }
      else if( ch=='M' )
        {
          return( 100 );
        }
      else if( ch=='R' )
        {
          return(  87 );
        }
      else if( ch=='F' )
        return(   9 );
        break;

      case('G'):  if( ch=='A' )
        {
          return( 31 );
        }
      else if( ch=='D' )
        {
          return( 64 );
        }
      else if( ch=='E' )
        return( 32 );
        break;

      case('H'):  if( ch=='E' )
        {
          return(  2 );
        }
      else if( ch=='F' )
        {
          return( 72 );
        }
      else if( ch=='G' )
        {
          return( 80 );
        }
      else if( ch=='O' )
        {
          return( 67 );
        }
      else if( ch==' ' )
        return(  1 );
        break;

      case('I'):  if( ch=='N' )
        {
          return( 49 );
        }
      else if( ch=='R' )
        {
          return( 77 );
        }
      else if( ch==' ' )
        return( 53 );
        break;

      case('K'):  if( ch=='R' )
        {
          return( 36 );
        }
      else if( ch==' ' )
        return( 19 );
        break;

      case('L'):  if( ch=='A' )
        {
          return(  57 );
        }
      else if( ch=='I' )
        {
          return(   3 );
        }
      else if( (ch=='R') || (ch=='W') )
        {
          return( 103 );
        }
      else if( ch=='U' )
        {
          return(  71 );
        }
      else if( ch==' ' )
        return(   1 );
        break;

      case('M'):  if( ch=='D' )
        {
          return( 101 );
        }
      else if( ch=='G' )
        {
          return(  12 );
        }
      else if( ch=='N' )
        {
          return(  25 );
        }
      else if( ch=='O' )
        return(  42 );
        break;

      case('N'):  switch( ch )
        {
        case('A'):  return(  11 );
        case('B'):  return(  41 );
        case('D'):  return(  60 );
        case('E'):  return(  10 );
        case('I'):  return(  28 );
        case('O'):  return( 102 );
        case('P'):  return(  93 );
        case(' '):  return(   7 );
        }
        break;

      case('O'):  if( ch=='S' )
        {
          return( 76 );
        }
      else if( ch==' ' )
        return( 8 );
        break;

      case('P'):  switch( ch )
        {
        case('A'):  return( 91 );
        case('B'):  return( 82 );
        case('D'):  return( 46 );
        case('M'):  return( 61 );
        case('O'):  return( 84 );
        case('R'):  return( 59 );
        case('T'):  return( 78 );
        case('U'):  return( 94 );
        case(' '):  return( 15 );
        }
        break;

      case('R'):  switch( ch )
        {
        case('A'):  return( 88 );
        case('B'):  return( 37 );
        case('E'):  return( 75 );
        case('H'):  return( 45 );
        case('N'):  return( 86 );
        case('U'):  return( 44 );
        }
        break;

      case('S'):  switch( ch )
        {
        case('B'):  return( 51 );
        case('C'):  return( 21 );
        case('E'):  return( 34 );
        case('I'):  return( 14 );
        case('M'):  return( 62 );
        case('N'):  return( 50 );
        case('R'):  return( 38 );
        case(' '):  return( 16 );
        }
        break;

      case('T'):  switch( ch )
        {
        case('A'):  return( 73 );
        case('B'):  return( 65 );
        case('C'):  return( 43 );
        case('E'):  return( 52 );
        case('H'):  return( 90 );
        case('I'):  return( 22 );
        case('L'):  return( 81 );
        case('M'):  return( 69 );
        }
        break;

      case('U'):  if( ch==' ' )
        return( 92 );
        break;

      case('V'):  if( ch==' ' )
        return( 23 );
        break;

      case('W'):  if( ch==' ' )
        return( 74 );
        break;

      case('X'):  if( ch=='E' )
        return( 54 );
        break;

      case('Y'):  if( ch=='B' )
        {
          return( 70 );
        }
      else if( ch==' ' )
        return( 39 );
        break;

      case('Z'):  if( ch=='N' )
        {
          return( 30 );
        }
      else if( ch=='R' )
        return( 40 );
        break;
      }

    if( (*ptr>='0') && (*ptr<='9') )
      if( (ch=='H') || (ch=='D') )
        return( 1 ); /* Hydrogen */

    return( 0 );
  }

  const char *OBChainsParser::ParseSmiles(const char *ptr, int prev)
  {
    const char *name;
    int atomid;
    int next;
    int type;
    int ch;

    type = 0;
    while( (ch = *ptr++) )
      {
        switch( ch )
          {
          case('-'): type = BF_SINGLE;
            break;
          case('='): type = BF_DOUBLE;
            break;
          case('#'): type = BF_TRIPLE;
            break;
          case('^'): type = BF_SINGLE|BF_AROMATIC;
            break;
          case('~'): type = BF_DOUBLE|BF_AROMATIC;
            break;

          case(')'): return( ptr );
          case('.'): prev = -1;
            break;
          case('('): ptr = ParseSmiles(ptr,prev);
            break;

          default:
            atomid = ch-'0';
            while( isdigit(*ptr) )
              atomid = (atomid*10)+(*ptr++)-'0';

            for( next=0; next<MonoAtomCount; next++ )
              if( MonoAtom[next].atomid == atomid )
                break;

            if( next == MonoAtomCount )
              {
                name = ChainsAtomName[atomid];
                MonoAtom[next].elem = IdentifyElement(name);
                MonoAtom[next].atomid = atomid;
                MonoAtom[next].bcount = 0;
                MonoAtomCount++;
              }

            if( prev != -1 )
              {
                MonoBond[MonoBondCount].flag = type;
                MonoBond[MonoBondCount].src = prev;
                MonoBond[MonoBondCount].dst = next;
                MonoBondCount++;

                MonoAtom[prev].bcount++;
                MonoAtom[next].bcount++;
              }
            prev = next;
          }
      }
    return( ptr-1 );
  }

} // end namespace OpenBabel

//! \file chains.cpp
//! \brief Parse for macromolecule chains and residues.
