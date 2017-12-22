// test_cpp.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <vector>
#include <random>
#include <cassert>

void SetupTestVectorWithRandomData(std::vector<int>& test_vector, size_t size)
{
	std::default_random_engine generator;
	std::uniform_int_distribution<int> distribution(1,100000);

	if( test_vector.size() > size )
	{
		test_vector.clear();
	}
	while( test_vector.size() < size )
	{
		test_vector.push_back(distribution(generator));
	}
}

bool IsSortedAscending(const std::vector<int>& test_vector)
{
	int last_known_value = 0;

	for( int i = 0, imax = test_vector.size(); i < imax; ++i )
	{
		if( i > 0 )
		{
			if( test_vector[i] < last_known_value )
			{
				return false;
			}
		}
		last_known_value = test_vector[i];
	}
	return true;
}

bool IsSortedDescending(const std::vector<int>& test_vector)
{
	int last_known_value = 0;

	for( int i = 0, imax = test_vector.size(); i < imax; ++i )
	{
		if( i > 0 )
		{
			if( test_vector[i] > last_known_value )
			{
				return false;
			}
		}
		last_known_value = test_vector[i];
	}
	return true;
}

class ClassWithCallback
{
public:
	ClassWithCallback(bool bSortAscending)
		:	m_bSortAscending( bSortAscending )
	{
	}

	int CompareMemberFunc(const void* a, const void* b)
	{
		if( m_bSortAscending )
		{
			return *static_cast<const int*>(a) - *static_cast<const int*>(b);
		}
		else
		{
			return *static_cast<const int*>(b) - *static_cast<const int*>(a);
		}
	}
private:
	bool m_bSortAscending;
};

typedef int (*LPFN_QSortCCallback)(const void* a, const void* b);
typedef int (ClassWithCallback::*LPFN_QSortMemberFunctionCallback)(const void* a, const void* b);

// this object holds the state for a C++ member function callback in memory
class QsortCallbackBase
{
public:
	// input: pointer to a unique C callback. 
	QsortCallbackBase(LPFN_QSortCCallback pCCallback)
		:	m_pClass( NULL ),
			m_pMethod( NULL ),
			m_pCCallback( pCCallback )
	{
	}

	// when done, remove allocation of the callback
	void Free()
	{
		m_pClass = NULL;
		// not clearing m_pMethod: it won't be used, since m_pClass is NULL and so this entry is marked as free
	}

	// when free, allocate this callback
	LPFN_QSortCCallback Reserve(ClassWithCallback* instance, LPFN_QSortMemberFunctionCallback method)
	{
		if( m_pClass )
			return NULL;

		m_pClass = instance;
		m_pMethod = method;
		return m_pCCallback;
	}

protected:
	static int StaticInvoke(int context, const void* a, const void* b);

private:
	LPFN_QSortCCallback m_pCCallback;
	ClassWithCallback* m_pClass;
	LPFN_QSortMemberFunctionCallback m_pMethod;
};

template <int context> class DynamicQSortCallback : public QsortCallbackBase
{
public:
	DynamicQSortCallback()
		:	QsortCallbackBase(&DynamicQSortCallback<context>::GeneratedStaticFunction)
	{
	}

private:
	static int GeneratedStaticFunction(const void* a, const void* b)
	{
		return StaticInvoke(context, a, b);
	}
};

class QSortMemberFunctionCallback
{
public:
	QSortMemberFunctionCallback(ClassWithCallback* instance, LPFN_QSortMemberFunctionCallback method);
	~QSortMemberFunctionCallback();

public:
	operator LPFN_QSortCCallback() const
	{
		return m_cbCallback;
	}

	bool IsValid() const
	{
		return m_cbCallback != NULL;
	}

private:
	LPFN_QSortCCallback m_cbCallback;
	int m_nAllocIndex;

private:
	QSortMemberFunctionCallback( const QSortMemberFunctionCallback& os );
	QSortMemberFunctionCallback& operator=( const QSortMemberFunctionCallback& os );
};

static QsortCallbackBase* AvailableCallbackSlots[] = {
	new DynamicQSortCallback<0x00>(),
	new DynamicQSortCallback<0x01>(),
	new DynamicQSortCallback<0x02>(),
	new DynamicQSortCallback<0x03>(),
	new DynamicQSortCallback<0x04>(),
	new DynamicQSortCallback<0x05>(),
	new DynamicQSortCallback<0x06>(),
	new DynamicQSortCallback<0x07>(),
	new DynamicQSortCallback<0x08>(),
	new DynamicQSortCallback<0x09>(),
	new DynamicQSortCallback<0x0A>(),
	new DynamicQSortCallback<0x0B>(),
	new DynamicQSortCallback<0x0C>(),
	new DynamicQSortCallback<0x0D>(),
	new DynamicQSortCallback<0x0E>(),
	new DynamicQSortCallback<0x0F>(),
};

int QsortCallbackBase::StaticInvoke(int context, const void* a, const void* b)
{
	return ((AvailableCallbackSlots[context]->m_pClass)->*(AvailableCallbackSlots[context]->m_pMethod))(a, b);
}


QSortMemberFunctionCallback::QSortMemberFunctionCallback(ClassWithCallback* instance, LPFN_QSortMemberFunctionCallback method)
{
	int imax = sizeof(AvailableCallbackSlots)/sizeof(AvailableCallbackSlots[0]);
	for( m_nAllocIndex = 0; m_nAllocIndex < imax; ++m_nAllocIndex )
	{
		m_cbCallback = AvailableCallbackSlots[m_nAllocIndex]->Reserve(instance, method);
		if( m_cbCallback != NULL )
			break;
	}
}

QSortMemberFunctionCallback::~QSortMemberFunctionCallback()
{
	if( IsValid() )
	{
		AvailableCallbackSlots[m_nAllocIndex]->Free();
	}
}

int _tmain(int argc, _TCHAR* argv[])
{
	std::vector<int> test;
	SetupTestVectorWithRandomData(test, 100);

	assert( !IsSortedAscending(test) );
	assert( !IsSortedDescending(test) );

	ClassWithCallback sortAscending(true), sortDescending(false);

	qsort( &test[0], test.size(), sizeof(int), QSortMemberFunctionCallback(&sortAscending, &ClassWithCallback::CompareMemberFunc));
	
	assert( IsSortedAscending(test) );

	qsort( &test[0], test.size(), sizeof(int), QSortMemberFunctionCallback(&sortDescending, &ClassWithCallback::CompareMemberFunc));
	
	assert( IsSortedDescending(test) );

	return 0;
}

