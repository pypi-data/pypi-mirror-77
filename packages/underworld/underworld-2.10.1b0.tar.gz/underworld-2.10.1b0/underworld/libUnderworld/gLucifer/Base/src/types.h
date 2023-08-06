/*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
**                                                                                  **
** This file forms part of the Underworld geophysics modelling application.         **
**                                                                                  **
** For full license and copyright information, please refer to the LICENSE.md file  **
** located at the project root, or contact the authors.                             **
**                                                                                  **
**~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*/


#ifndef __lucBase_types_h__
#define __lucBase_types_h__

typedef struct lucColourMap                lucColourMap;
typedef struct lucColour                   lucColour;
typedef struct lucColourMapping            lucColourMapping;

typedef struct lucDatabase                 lucDatabase;

typedef struct lucDrawingObject            lucDrawingObject;

/* types for clarity */
typedef Index Colour_Index;
typedef Index DrawingObject_Index;

typedef enum
{
   lucLeftHanded = -1,
   lucRightHanded = 1
} lucCoordinateSystem;

#endif
