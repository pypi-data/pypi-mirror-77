/*
 * Memory allocation functions for testing
 *
 * Copyright (C) 2014-2020, Joachim Metz <joachim.metz@gmail.com>
 *
 * Refer to AUTHORS for acknowledgements.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

#if !defined( _VSLVM_TEST_MEMORY_H )
#define _VSLVM_TEST_MEMORY_H

#include <common.h>

#if defined( __cplusplus )
extern "C" {
#endif

#if defined( HAVE_GNU_DL_DLSYM ) && defined( __GNUC__ ) && !defined( LIBVSLVM_DLL_IMPORT ) && !defined( __arm__ ) && !defined( __clang__ ) && !defined( __CYGWIN__ ) && !defined( __hppa__ ) && !defined( __mips__ ) && !defined( __sparc__ ) && !defined( HAVE_ASAN )
#define HAVE_VSLVM_TEST_MEMORY		1
#endif

#if defined( HAVE_VSLVM_TEST_MEMORY )

extern int vslvm_test_malloc_attempts_before_fail;

extern int vslvm_test_memcpy_attempts_before_fail;

extern int vslvm_test_memset_attempts_before_fail;

extern int vslvm_test_realloc_attempts_before_fail;

#endif /* defined( HAVE_VSLVM_TEST_MEMORY ) */

#if defined( __cplusplus )
}
#endif

#endif /* !defined( _VSLVM_TEST_MEMORY_H ) */

